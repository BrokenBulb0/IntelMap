import pydeck as pdk
import pandas as pd

def create_3d_map(data, map_style="mapbox://styles/mapbox/dark-v10", radius=100, opacity=0.8, tooltip=None):
    """
    Create a 3D map visualization using PyDeck
    
    Args:
        data (pd.DataFrame): DataFrame containing message data with lat/lon coordinates
        map_style (str): Mapbox style URL
        radius (int): Size of the point markers
        opacity (float): Opacity of the point markers
        tooltip (dict): PyDeck tooltip configuration
        
    Returns:
        pdk.Deck: PyDeck map object
    """
    # Set initial view state
    view_state = pdk.ViewState(
        latitude=data["latitude"].mean(),
        longitude=data["longitude"].mean(),
        zoom=3,
        pitch=45,  # Gives 3D perspective
        bearing=0
    )
    
    # Create scatterplot layer for messages
    scatterplot_layer = pdk.Layer(
        "ScatterplotLayer",
        data=data.to_dict(orient="records"),
        get_position=["longitude", "latitude"],
        get_color=[255, 140, 0, 200],  # Orange points
        get_radius=radius,
        pickable=True,
        opacity=opacity,
        stroked=True,
        filled=True,
        wireframe=True,
        extruded=True,
        elevation_scale=0,
        get_elevation=0
    )
    
    # Create the deck
    deck = pdk.Deck(
        layers=[scatterplot_layer],
        initial_view_state=view_state,
        map_style=map_style,
        tooltip=tooltip
    )
    
    return deck

def create_tooltip():
    """
    Create a tooltip configuration for PyDeck
    
    Returns:
        dict: PyDeck tooltip configuration
    """
    return {
        "html": "<b>{location_name}</b><br/>"
                "<i>{timestamp}</i><br/>"
                "{text}",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }

def create_callout_layer(data, selected_points):
    """
    Create a callout layer to highlight selected points
    
    Args:
        data (pd.DataFrame): DataFrame containing message data
        selected_points (list): List of selected point IDs
        
    Returns:
        pdk.Layer: PyDeck layer highlighting selected points
    """
    # Filter data to only selected points
    if not selected_points:
        return None
        
    selected_data = data[data['id'].isin(selected_points)]
    
    callout_layer = pdk.Layer(
        "ScatterplotLayer",
        selected_data.to_dict(orient="records"),
        get_position=["longitude", "latitude"],
        get_color=[255, 0, 0, 200],  # Red for selected points
        get_radius=150,
        pickable=True,
        opacity=0.9,
        stroked=True,
        filled=True,
        wireframe=True,
        line_width_min_pixels=2
    )
    
    return callout_layer
