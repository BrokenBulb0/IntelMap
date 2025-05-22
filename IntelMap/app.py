
# ----------------- Imports -----------------

import streamlit as st
import pandas as pd
import pydeck as pdk
import os
import base64
from datetime import datetime, timezone
import humanize
import sqlite3
import plotly.express as px
import spacy
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable, GeocoderTimedOut

from config import MEDIA_DIR, DB_PATH


# ----------------- Location Extraction Utilities -----------------

# Load NLP model for location extraction
nlp = spacy.load("en_core_web_sm")
geolocator = Nominatim(user_agent="telegram-map")

def extract_places(text):
    doc = nlp(text)
    return [ent.text for ent in doc.ents if ent.label_ in ("GPE", "LOC")]

@st.cache_data(show_spinner=False)
def geocode_place(place):
    try:
        location = geolocator.geocode(place, timeout=5)
        if location:
            return location.latitude, location.longitude, location.address
    except (GeocoderUnavailable, GeocoderTimedOut):
        return None, None, None
    return None, None, None


# ----------------- Load Data with Fallback Geolocation -----------------

@st.cache_data(ttl=60)
def load_data():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            query = '''
                SELECT DISTINCT
                    m.id, m.text, m.timestamp, m.media_paths,
                    l.lat AS latitude, l.lon AS longitude, 
                    COALESCE(l.location_name, 'Ubicación desconocida') AS location_name
                FROM messages m
                LEFT JOIN locations l ON m.id = l.message_id
                WHERE m.timestamp > datetime('now', '-3 days')
                GROUP BY m.id
                ORDER BY m.timestamp DESC
                LIMIT 500
            '''
            df = pd.read_sql(query, conn)

        if df.empty:
            return df

        df = df[
            (df['latitude'].between(-90, 90)) & 
            (df['longitude'].between(-180, 180)) |
            (df['latitude'].isna()) |
            (df['longitude'].isna())
        ].copy()

        df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
        df['time_ago'] = (datetime.now(timezone.utc) - df['timestamp']).apply(humanize.naturaltime)
        df['location_name'] = df['location_name'].str.title()
        df['flag'] = None  # Placeholder

        # Fallback location detection via NER + geocode
        for i, row in df.iterrows():
            if pd.isna(row['latitude']) or pd.isna(row['longitude']):
                places = extract_places(row['text'] or "")
                for place in places:
                    lat, lon, resolved = geocode_place(place)
                    if lat and lon:
                        df.at[i, 'latitude'] = lat
                        df.at[i, 'longitude'] = lon
                        df.at[i, 'location_name'] = resolved or place.title()
                        break

        # Drop rows that still have no valid coordinates
        df = df[
            (df['latitude'].notna()) & (df['longitude'].notna()) &
            (df['latitude'].between(-90, 90)) & (df['longitude'].between(-180, 180))
        ].copy()

        return df
    except Exception as e:
        st.error(f"Error cargando datos: {str(e)}")
        return pd.DataFrame()


# ----------------- Media Renderer -----------------
def render_media(media_paths):
    if not media_paths:
        return
    media_files = media_paths.split(",")
    for media_file in media_files:
        media_file = media_file.strip()
        media_path = os.path.join(MEDIA_DIR, media_file)
        if media_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            st.image(media_path, caption="Imagen del mensaje")
        elif media_file.lower().endswith(('.mp4', '.webm', '.mov')):
            st.video(media_path)

# ----------------- Session State Init -----------------
if "selected_points" not in st.session_state:
    st.session_state.selected_points = []

if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = datetime.now()

if "map_zoom" not in st.session_state:
    st.session_state.map_zoom = 6

if "map_style" not in st.session_state:
    st.session_state.map_style = "mapbox://styles/mapbox/satellite-streets-v11"

# ----------------- Title -----------------
st.set_page_config(page_title="Telegram Messages Map", page_icon="🌎", layout="wide")
st.title("🛰️ Mapa de Mensajes de Telegram")
st.markdown("Visualización geoespacial de mensajes con medios e inteligencia contextual")

# ----------------- Sidebar -----------------
with st.sidebar:
    st.header("Controles")
    st.info(f"Última carga: {st.session_state.last_refresh.strftime('%Y-%m-%d %H:%M:%S')}")

    st.subheader("Configuración del Mapa")
    base_radius = st.slider("Tamaño base de punto", 10, 200, 50)
    point_opacity = st.slider("Opacidad", 0.1, 1.0, 0.8)
    zoom_slider = st.slider("Nivel de zoom inicial", 1, 15, st.session_state.map_zoom)
    st.session_state.map_zoom = zoom_slider

    map_style_options = {
        "Satellite Streets": "mapbox://styles/mapbox/satellite-streets-v11",
        "Light": "mapbox://styles/mapbox/light-v10",
        "Dark": "mapbox://styles/mapbox/dark-v10",
        "Outdoors": "mapbox://styles/mapbox/outdoors-v11",
        "Streets": "mapbox://styles/mapbox/streets-v11"
    }
    selected_style = st.selectbox("Estilo del mapa", list(map_style_options.keys()))
    st.session_state.map_style = map_style_options[selected_style]

    st.subheader("Generar Reporte")
    if len(st.session_state.selected_points) > 0:
        if st.button("Generar Reporte"):
            report_df = pd.DataFrame(st.session_state.selected_points)
            st.session_state.report = {
                "total_messages": len(report_df),
                "date_range": f"{report_df['timestamp'].min().date()} — {report_df['timestamp'].max().date()}",
                "locations": sorted(report_df['location_name'].unique()),
                "message_df": report_df,
                "map_fig": px.scatter_mapbox(
                    report_df,
                    lat="latitude",
                    lon="longitude",
                    hover_name="location_name",
                    hover_data=["text"],
                    color_discrete_sequence=["red"],
                    zoom=4,
                    height=400
                ).update_layout(mapbox_style="carto-darkmatter", margin={"r":0,"t":0,"l":0,"b":0})
            }
            st.success("Reporte generado")

    if st.button("Limpiar Selección"):
        st.session_state.selected_points = []
        st.session_state.report = {}
        st.session_state.pop("map_center", None)

# ----------------- Data Load -----------------
data = load_data()

# ----------------- Auto-Center -----------------
if "map_center" not in st.session_state:
    flagged = data[data['flag'].isin(['alert', 'highlight', 'important'])] if 'flag' in data.columns else pd.DataFrame()
    if not flagged.empty:
        st.session_state.map_center = {
            "lat": flagged.iloc[0]["latitude"],
            "lon": flagged.iloc[0]["longitude"]
        }

# ----------------- Main Layout -----------------
col1, col2 = st.columns([7, 3])

with col1:
    st.subheader("🗺️ Mapa 3D de Mensajes")

    if not data.empty:
        center_lat = data["latitude"].mean()
        center_lon = data["longitude"].mean()
        if "map_center" in st.session_state:
            center_lat = st.session_state.map_center["lat"]
            center_lon = st.session_state.map_center["lon"]

        zoom_level = st.session_state.map_zoom
        adjusted_radius = base_radius * (2 ** (zoom_level - 10))

        layer = pdk.Layer(
            "ScatterplotLayer",
            data=data,
            get_position=["longitude", "latitude"],
            get_radius=adjusted_radius,
            get_fill_color=[255, 87, 51, int(point_opacity * 255)],
            pickable=True,
            radius_units="meters"
        )

        view_state = pdk.ViewState(
            latitude=center_lat,
            longitude=center_lon,
            zoom=zoom_level,
            pitch=45
        )

        r = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            map_style=st.session_state.map_style,
            tooltip={"text": "{location_name}\n{text}"}
        )
        st.pydeck_chart(r)
    else:
        st.warning("No hay datos para mostrar")

with col2:
    st.subheader("📩 Detalles del Mensaje")
    if not data.empty:
        options = [f"{row['location_name']}: {row['text'][:30]}..." for _, row in data.iterrows()]
        idx = st.selectbox("Selecciona un mensaje", options=range(len(options)), format_func=lambda i: options[i])
        selected = data.iloc[idx]

        st.markdown(f"**Ubicación:** {selected['location_name']}")
        st.markdown(f"**Tiempo:** {selected['time_ago']}")
        st.markdown(f"**Mensaje:**")
        st.markdown(selected['text'])

        render_media(selected.get('media_paths'))

        if st.button("Agregar al Reporte"):
            exists = any(p['id'] == selected['id'] for p in st.session_state.selected_points)
            if not exists:
                st.session_state.selected_points.append(selected.to_dict())
                st.success("Agregado")
            else:
                st.warning("Ya está en la selección")

        if st.button("Centrar en el Mapa"):
            st.session_state.map_center = {
                "lat": selected["latitude"],
                "lon": selected["longitude"]
            }
            st.rerun()
    else:
        st.info("No hay mensajes disponibles")

    if st.session_state.selected_points:
        st.subheader(f"📝 Seleccionados ({len(st.session_state.selected_points)})")
        for i, p in enumerate(st.session_state.selected_points):
            st.markdown(f"{i+1}. **{p['location_name']}**: {p['text'][:50]}...")

# ----------------- Report Section -----------------
if "report" in st.session_state and st.session_state.report:
    st.header("📊 Reporte Generado")

    st.subheader("Resumen")
    st.markdown(f"**Total de mensajes:** {st.session_state.report['total_messages']}")
    st.markdown(f"**Rango de fechas:** {st.session_state.report['date_range']}")
    st.markdown(f"**Ubicaciones:** {', '.join(st.session_state.report['locations'])}")

    st.subheader("Mapa de Selección")
    st.plotly_chart(st.session_state.report['map_fig'], use_container_width=True)

    st.subheader("Mensajes")
    st.dataframe(st.session_state.report['message_df'])

    csv = st.session_state.report['message_df'].to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="telegram_report.csv">📥 Descargar CSV</a>'
    st.markdown(href, unsafe_allow_html=True)
