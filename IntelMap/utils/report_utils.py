import pandas as pd
import plotly.express as px
from datetime import datetime

def generate_report(data):
    """
    Generate a report based on selected map points
    
    Args:
        data (pd.DataFrame): DataFrame containing selected message data
        
    Returns:
        dict: Dictionary containing report components
    """
    # Create a copy of the data to avoid modifying the original
    report_data = data.copy()
    
    # Ensure datetime format for timestamp
    if 'timestamp' in report_data.columns:
        report_data['timestamp'] = pd.to_datetime(report_data['timestamp'])
    
    # Create summary statistics
    total_messages = len(report_data)
    
    # Get date range
    if 'timestamp' in report_data.columns and not report_data.empty:
        min_date = report_data['timestamp'].min().strftime('%Y-%m-%d')
        max_date = report_data['timestamp'].max().strftime('%Y-%m-%d')
        date_range = f"{min_date} to {max_date}"
    else:
        date_range = "N/A"
    
    # Get unique locations
    if 'location_name' in report_data.columns:
        locations = report_data['location_name'].unique().tolist()
    else:
        locations = []
    
    # Create a map visualization of the selected points
    if not report_data.empty and 'latitude' in report_data.columns and 'longitude' in report_data.columns:
        fig = px.scatter_mapbox(
            report_data,
            lat="latitude",
            lon="longitude",
            hover_name="location_name",
            hover_data=["text", "timestamp"],
            color_discrete_sequence=["fuchsia"],
            zoom=1,
            height=400
        )
        fig.update_layout(
            mapbox_style="open-street-map",
            margin={"r": 0, "t": 0, "l": 0, "b": 0}
        )
    else:
        # Create empty figure if no data
        fig = px.scatter_mapbox(
            pd.DataFrame({'lat': [0], 'lon': [0], 'text': ['No data']}),
            lat="lat",
            lon="lon",
            hover_name="text",
            zoom=1,
            height=400
        )
        fig.update_layout(
            mapbox_style="open-street-map",
            margin={"r": 0, "t": 0, "l": 0, "b": 0}
        )
    
    # Prepare message dataframe for display
    if not report_data.empty:
        message_df = report_data[['location_name', 'text', 'timestamp']].copy()
        if 'timestamp' in message_df.columns:
            message_df['timestamp'] = message_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
        message_df.columns = ['Location', 'Message', 'Time']
    else:
        message_df = pd.DataFrame(columns=['Location', 'Message', 'Time'])
    
    # Assemble the report
    report = {
        'total_messages': total_messages,
        'date_range': date_range,
        'locations': locations,
        'map_fig': fig,
        'message_df': message_df,
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return report
