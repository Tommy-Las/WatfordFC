import pandas as pd
import numpy as np

def get_speed_metrics(df, player_name, session_data):
    """Get speed metrics for a player's session."""
    if session_data.empty:
        return {
            'Max Speed': 0.0,
            'Avg Speed Season': 0.0,
            '% Max Speed': 0.0,
            'Max Speed Season': 0.0
        }
    
    return {
        'Max Speed': float(session_data['Max Speed'].iloc[0]),
        'Avg Speed Season': float(session_data['Avg Speed Season'].iloc[0]),
        '% Max Speed': float(session_data['% Max Speed'].iloc[0]),
        'Max Speed Season': float(session_data['Max Speed Season'].iloc[0])
    }

def get_speed_summary(session_data):
    """Get speed-related metrics summary."""
    if session_data.empty:
        return {
            'Max Speed': 0.0,
            'Avg Speed Season': 0.0,
            '% Max Speed': 0.0,
            'Max Speed Season': 0.0
        }
    
    return {
        'Max Speed': float(session_data['Max Speed'].max()),
        'Avg Speed Season': float(session_data['Avg Speed Season'].mean()),
        '% Max Speed': float(session_data['% Max Speed'].mean()),
        'Max Speed Season': float(session_data['Max Speed Season'].max())
    }