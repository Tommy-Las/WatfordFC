import pandas as pd
import numpy as np

def calculate_relative_distance_metrics(df, player_id, session_data):
    """Calculate relative distance metrics for a player."""
    player_data = df[df['player_id'] == player_id]
    
    # Calculate all-time max values for relative calculations
    all_time_max_distance = float(player_data['distance'].max())
    
    # Get current session values
    current_distance = float(session_data['distance'].iloc[0])
    
    return {
        'total_distance': current_distance,
        'relative_distance': (current_distance / all_time_max_distance * 100)
    }

def get_distance_summary(session_data):
    """Get distance-related metrics summary."""
    if session_data.empty:
        return {
            'total_distance': 0.0,
            'relative_distance': 0.0
        }
    
    return {
        'total_distance': float(session_data['distance'].sum()),
        'relative_distance': 100.0
    }