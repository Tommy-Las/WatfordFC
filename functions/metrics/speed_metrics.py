import pandas as pd
import numpy as np

def calculate_relative_speed_metrics(df, player_id, session_data):
    """Calculate relative speed metrics for a player."""
    player_data = df[df['player_id'] == player_id]
    
    # Calculate all-time max values for relative calculations
    all_time_max_speed = float(player_data['max_speed'].max())
    all_time_max_avg_speed = float(player_data['avg_speed'].max())
    
    # Get current session values
    current_max_speed = float(session_data['max_speed'].iloc[0])
    current_avg_speed = float(session_data['avg_speed'].iloc[0])
    
    return {
        'max_speed': current_max_speed,
        'avg_speed': current_avg_speed,
        'relative_max_speed': (current_max_speed / all_time_max_speed * 100),
        'relative_avg_speed': (current_avg_speed / all_time_max_avg_speed * 100)
    }

def get_speed_summary(session_data):
    """Get speed-related metrics summary."""
    if session_data.empty:
        return {
            'max_speed': 0.0,
            'avg_speed': 0.0,
            'relative_max_speed': 0.0,
            'relative_avg_speed': 0.0
        }
    
    return {
        'max_speed': float(session_data['max_speed'].max()),
        'avg_speed': float(session_data['avg_speed'].mean()),
        'relative_max_speed': 100.0,  # Current session's max is 100% of itself
        'relative_avg_speed': 100.0   # Current session's avg is 100% of itself
    }