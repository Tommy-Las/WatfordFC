import pandas as pd
import numpy as np

def get_distance_metrics(df, player_name, session_data):
    """Get distance metrics for a player's session."""
    if session_data.empty:
        return {
            'total_distance': 0.0,
            'relative_distance': 0.0
        }
    
    return {
        'total_distance': float(session_data['distance'].iloc[0]),
        'relative_distance': float(session_data['relative_distance'].iloc[0])
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
        'relative_distance': float(session_data['relative_distance'].mean())
    }