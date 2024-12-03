import pandas as pd
import numpy as np

def calculate_relative_acceleration_metrics(df, player_id, session_data):
    """Calculate relative acceleration metrics for a player."""
    player_data = df[df['player_id'] == player_id]
    
    # Calculate all-time max values for relative calculations
    all_time_max_accel = float(player_data['max_acceleration'].max())
    all_time_max_decel = abs(float(player_data['max_deceleration'].min()))
    
    # Get current session values
    current_max_accel = float(session_data['max_acceleration'].iloc[0])
    current_max_decel = abs(float(session_data['max_deceleration'].iloc[0]))
    
    return {
        'max_acceleration': current_max_accel,
        'max_deceleration': current_max_decel,
        'relative_acceleration': (current_max_accel / all_time_max_accel * 100),
        'relative_deceleration': (current_max_decel / all_time_max_decel * 100)
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
        'relative_acceleration': 100.0,
        'relative_deceleration': 100.0
    }