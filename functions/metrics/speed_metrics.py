import pandas as pd
import numpy as np

def get_speed_metrics(df, player_name, session_data):
    """Get speed metrics for a player's session."""
    if session_data.empty:
        return {
            'max_speed': 0.0,
            'avg_speed': 0.0,
            'relative_max_speed': 0.0,
            'season_max_speed': 0.0
        }
    
    return {
        'max_speed': float(session_data['max_speed'].iloc[0]),
        'avg_speed': float(session_data['avg_speed'].iloc[0]),
        'relative_max_speed': float(session_data['relative_max_speed'].iloc[0]),
        'season_max_speed': float(session_data['season_max_speed'].iloc[0])
    }

def get_speed_summary(session_data):
    """Get speed-related metrics summary."""
    if session_data.empty:
        return {
            'max_speed': 0.0,
            'avg_speed': 0.0,
            'relative_max_speed': 0.0,
            'season_max_speed': 0.0
        }
    
    return {
        'max_speed': float(session_data['max_speed'].max()),
        'avg_speed': float(session_data['avg_speed'].mean()),
        'relative_max_speed': float(session_data['relative_max_speed'].mean()),
        'season_max_speed': float(session_data['season_max_speed'].max())
    }