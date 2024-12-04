import pandas as pd
import numpy as np

def get_distance_metrics(df, player_name, session_data):
    """Get distance metrics for a player's session."""
    if session_data.empty:
        return {
            'TD': 0.0,
            'TD_Rel': 0.0
        }
    
    return {
        'TD': float(session_data['TD'].iloc[0]),
        'TD_Rel': float(session_data['TD_Rel'].iloc[0])
    }

def get_distance_summary(session_data):
    """Get distance-related metrics summary."""
    if session_data.empty:
        return {
            'TD': 0.0,
            'TD_Rel': 0.0
        }
    
    return {
        'TD': float(session_data['TD'].sum()),
        'TD_Rel': float(session_data['TD_Rel'].mean())
    }