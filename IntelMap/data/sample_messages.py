def get_sample_messages():
    """
    Provide sample message data for the MVP version
    
    In a production environment, this would be replaced with actual Telegram API data
    
    Returns:
        list: List of dictionaries containing sample message data
    """
    sample_messages = [
        {
            "id": "msg1",
            "text": "Traffic accident reported on Main Street. Two vehicles involved, minor injuries.",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "location_name": "New York City",
            "timestamp": "2023-09-15 14:30:00",
            "image_url": "https://images.unsplash.com/photo-1546984575-757f4f7c13cf?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8dHJhZmZpYyUyMGphbXxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=800&q=60"
        },
        {
            "id": "msg2",
            "text": "Protest scheduled for tomorrow at City Hall. Expect road closures from 10 AM to 2 PM.",
            "latitude": 34.0522,
            "longitude": -118.2437,
            "location_name": "Los Angeles",
            "timestamp": "2023-09-15 15:45:00",
            "image_url": "https://images.unsplash.com/photo-1582896911227-c966f6001414?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8cHJvdGVzdHxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=800&q=60"
        },
        {
            "id": "msg3",
            "text": "Flash flood warning in effect until 8 PM tonight. Avoid downtown area.",
            "latitude": 29.7604,
            "longitude": -95.3698,
            "location_name": "Houston",
            "timestamp": "2023-09-15 16:15:00",
            "image_url": "https://images.unsplash.com/photo-1593978301851-40c1849d47d4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8Zmxvb2R8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=800&q=60"
        },
        {
            "id": "msg4",
            "text": "Power outage affecting north side of the city. Crews working to restore service.",
            "latitude": 41.8781,
            "longitude": -87.6298,
            "location_name": "Chicago",
            "timestamp": "2023-09-15 17:00:00",
            "image_url": "https://images.unsplash.com/photo-1621188988909-fbef0a88dc04?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8cG93ZXIlMjBvdXRhZ2V8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=800&q=60"
        },
        {
            "id": "msg5",
            "text": "Three-alarm fire at warehouse on Industrial Blvd. Please avoid the area.",
            "latitude": 33.4484,
            "longitude": -112.0740,
            "location_name": "Phoenix",
            "timestamp": "2023-09-15 18:30:00",
            "image_url": "https://images.unsplash.com/photo-1589641896430-8ffaa8377f92?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8ZmlyZSUyMGJ1aWxkaW5nfGVufDB8fDB8fHww&auto=format&fit=crop&w=800&q=60"
        },
        {
            "id": "msg6",
            "text": "Public transportation disruption. Subway line A closed between stations 5-8 due to maintenance.",
            "latitude": 37.7749,
            "longitude": -122.4194,
            "location_name": "San Francisco",
            "timestamp": "2023-09-15 19:45:00",
            "image_url": "https://images.unsplash.com/photo-1545472956-85a12c3fa78c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8c3Vid2F5JTIwc3RhdGlvbnxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=800&q=60"
        },
        {
            "id": "msg7",
            "text": "Severe weather alert: Thunderstorms expected this evening with possible hail.",
            "latitude": 39.9526,
            "longitude": -75.1652,
            "location_name": "Philadelphia",
            "timestamp": "2023-09-15 20:15:00",
            "image_url": "https://images.unsplash.com/photo-1594760467013-64ac2b80b7d3?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8dGh1bmRlcnN0b3JtfGVufDB8fDB8fHww&auto=format&fit=crop&w=800&q=60"
        },
        {
            "id": "msg8",
            "text": "Water main break on Elm Street. Residents may experience low water pressure.",
            "latitude": 32.7767,
            "longitude": -96.7970,
            "location_name": "Dallas",
            "timestamp": "2023-09-15 21:00:00",
            "image_url": "https://images.unsplash.com/photo-1631469171718-fd64444d3d5d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8d2F0ZXIlMjBtYWluJTIwYnJlYWt8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=800&q=60"
        },
        {
            "id": "msg9",
            "text": "Community meeting regarding new development project scheduled for next Tuesday at 7 PM in City Hall.",
            "latitude": 47.6062,
            "longitude": -122.3321,
            "location_name": "Seattle",
            "timestamp": "2023-09-15 22:30:00",
            "image_url": "https://images.unsplash.com/photo-1577481489966-ba3033b1e2e1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8Y29tbXVuaXR5JTIwbWVldGluZ3xlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=800&q=60"
        },
        {
            "id": "msg10",
            "text": "Road construction beginning tomorrow on Highway 101. Expect delays for the next two weeks.",
            "latitude": 42.3601,
            "longitude": -71.0589,
            "location_name": "Boston",
            "timestamp": "2023-09-15 23:45:00",
            "image_url": "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8cm9hZCUyMGNvbnN0cnVjdGlvbnxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=800&q=60"
        },
        {
            "id": "msg11",
            "text": "Local charity drive collecting donations at Central Park. Food, clothing, and toys needed.",
            "latitude": 30.2672,
            "longitude": -97.7431,
            "location_name": "Austin",
            "timestamp": "2023-09-16 09:15:00",
            "image_url": "https://images.unsplash.com/photo-1532629345422-7515f3d16bb6?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8ZG9uYXRpb258ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=800&q=60"
        },
        {
            "id": "msg12",
            "text": "School closure announcement: All public schools will be closed tomorrow due to expected severe weather.",
            "latitude": 39.7392,
            "longitude": -104.9903,
            "location_name": "Denver",
            "timestamp": "2023-09-16 10:30:00",
            "image_url": "https://images.unsplash.com/photo-1580582932707-520aed937b7b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8c2Nob29sJTIwY2xvc2VkfGVufDB8fDB8fHww&auto=format&fit=crop&w=800&q=60"
        }
    ]
    
    return sample_messages
