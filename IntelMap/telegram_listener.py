import asyncio
import sqlite3
import logging
import os
from datetime import datetime
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import spacy
from config import CHANNELS, MONITOR_GROUP, MEDIA_DIR, DB_PATH, LOG_DIR
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, 'listener.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('TelegramListener')

# Inicialización NLP y Geocoder
nlp = spacy.load("en_core_web_sm")
geolocator = Nominatim(user_agent="intel_map_app_v2")

# Base de datos
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY,
        text TEXT NOT NULL,
        media_paths TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        source_channel TEXT,
        telegram_msg_id INTEGER
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS locations (
        id INTEGER PRIMARY KEY,
        message_id INTEGER,
        lat REAL,
        lon REAL,
        location_name TEXT,
        confidence REAL,
        FOREIGN KEY(message_id) REFERENCES messages(id)
    )
''')
conn.commit()

def extract_flags(text: str) -> list:
    """Extrae códigos de país de emojis de banderas"""
    flags = []
    i = 0
    while i < len(text):
        if 0x1F1E6 <= ord(text[i]) <= 0x1F1FF:
            if i+1 < len(text) and 0x1F1E6 <= ord(text[i+1]) <= 0x1F1FF:
                flags.append(f"{chr(ord(text[i]) - 0x1F1E6 + 65)}"
                           f"{chr(ord(text[i+1]) - 0x1F1E6 + 65)}")
                i += 2
                continue
        i += 1
    return flags

async def geocode_with_retry(location: str, country_code: str = None, retries=3) -> tuple:
    """Geocodificación con reintentos y contexto de país"""
    for attempt in range(retries):
        try:
            query = f"{location}, {country_code}" if country_code else location
            result = geolocator.geocode(query, exactly_one=True)
            if result:
                logger.debug(f"Geocode success: {query} -> {result.latitude},{result.longitude}")
                return (result.latitude, result.longitude), 0.9 - (0.2 * attempt)
            return None, 0.0
        except (GeocoderTimedOut, GeocoderUnavailable) as e:
            logger.warning(f"Geocode attempt {attempt+1} failed: {e}")
            await asyncio.sleep(2 ** attempt)
    return None, 0.0

async def process_message(message):
    """Procesa un mensaje y extrae ubicaciones"""
    try:
        text = message.text or ""
        logger.info(f"Processing message: {text[:50]}...")
        
        flags = extract_flags(text)
        doc = nlp(text)
        locations = [ent.text for ent in doc.ents if ent.label_ in ['GPE', 'LOC']]
        
        results = []
        
        for loc in locations:
            best_coords = None
            best_confidence = 0.0
            
            # Intentar con códigos de país primero
            for cc in flags:
                coords, confidence = await geocode_with_retry(loc, cc)
                if confidence > best_confidence:
                    best_coords = coords
                    best_confidence = confidence
            
            # Si no se encontró con bandera, intentar sin
            if not best_coords:
                coords, confidence = await geocode_with_retry(loc)
                if confidence > best_confidence:
                    best_coords = coords
                    best_confidence = confidence
            
            if best_coords:
                results.append({
                    'name': loc,
                    'lat': best_coords[0],
                    'lon': best_coords[1],
                    'confidence': best_confidence
                })
        
        return results
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        return []

async def main():
    """Función principal del listener"""
    client = TelegramClient(
        'intel_map_session',
        int(os.getenv('API_ID')),
        os.getenv('API_HASH')
    )
    
    try:
        await client.start()
        logger.info("Client started successfully")
        
        @client.on(events.NewMessage(chats=CHANNELS))
        async def handler(event):
            try:
                start_time = datetime.now()
                logger.info(f"New message from {event.chat_id}")
                
                # Guardar en DB primero
                media_paths = []
                if event.message.media:
                    filename = f"{event.chat_id}_{event.message.id}"
                    path = await event.message.download_media(
                        file=os.path.join(MEDIA_DIR, filename)
                    )
                    media_paths.append(path)
                    logger.debug(f"Media saved: {path}")
                
                c.execute('''
                    INSERT INTO messages 
                    (text, media_paths, source_channel, telegram_msg_id)
                    VALUES (?, ?, ?, ?)
                ''', (
                    event.message.text,
                    ','.join(media_paths),
                    str(event.chat_id),
                    event.message.id
                ))
                msg_id = c.lastrowid
                conn.commit()
                logger.debug(f"Message saved to DB: ID {msg_id}")
                
                # Forward al grupo privado
                target_entity = await client.get_entity(MONITOR_GROUP)
                await event.message.forward_to(target_entity)
                logger.info(f"Message {msg_id} forwarded to monitor group")
                
                # Procesamiento de ubicaciones
                locations = await process_message(event.message)
                for loc in locations:
                    c.execute('''
                        INSERT INTO locations 
                        (message_id, lat, lon, location_name, confidence)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        msg_id,
                        loc['lat'],
                        loc['lon'],
                        loc['name'],
                        loc['confidence']
                    ))
                conn.commit()
                
                logger.info(f"Processing completed in {datetime.now() - start_time}")
                
            except FloodWaitError as e:
                logger.error(f"Flood wait required: {e.seconds} seconds")
                await asyncio.sleep(e.seconds)
            except Exception as e:
                logger.error(f"Error handling message: {str(e)}")
                conn.rollback()
        
        logger.info("Starting listener...")
        await client.run_until_disconnected()
        
    except Exception as e:
        logger.critical(f"Fatal error: {str(e)}")
    finally:
        await client.disconnect()
        conn.close()
        logger.info("Shutdown complete")

if __name__ == '__main__':
    asyncio.run(main())