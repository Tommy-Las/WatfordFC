import pandas as pd
import numpy as np

def get_acceleration_metrics(df, player_name, session_data):
    """Get acceleration metrics for a player's session."""
    if session_data.empty:
        return {
            'max_acceleration': 0.0,
            'max_deceleration': 0.0,
            'relative_acceleration': 0.0,
            'relative_deceleration': 0.0
        }
    
    return {
        'max_acceleration': float(session_data['max_acceleration'].iloc[0]),
        'max_deceleration': float(session_data['max_deceleration'].iloc[0]),
        'relative_acceleration': float(session_data['relative_acceleration'].iloc[0]),
        'relative_deceleration': float(session_data['relative_deceleration'].iloc[0])
    }

def get_acceleration_summary(session_data):
    """Get acceleration-related metrics summary."""
    if session_data.empty:
        return {
            'max_acceleration': 0.0,
            'max_deceleration': 0.0,
            'relative_acceleration': 0.0,
            'relative_deceleration': 0.0
        }
    
    return {
        'max_acceleration': float(session_data['max_acceleration'].max()),
        'max_deceleration': float(session_data['max_deceleration'].min()),
        'relative_acceleration': float(session_data['relative_acceleration'].mean()),
        'relative_deceleration': float(session_data['relative_deceleration'].mean())
    }