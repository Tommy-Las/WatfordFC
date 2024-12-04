import pandas as pd
import numpy as np

def get_acceleration_metrics(df, player_name, session_data):
    """Get acceleration metrics for a player's session."""
    if session_data.empty:
        return {
            'ACC': 0.0,
            'DEC': 0.0,
            'ACC_Rel': 0.0,
            'DEC_Rel': 0.0
        }
    
    return {
        'ACC': float(session_data['ACC'].iloc[0]),
        'DEC': float(session_data['DEC'].iloc[0]),
        'ACC_Rel': float(session_data['ACC_Rel'].iloc[0]),
        'DEC_Rel': float(session_data['DEC_Rel'].iloc[0])
    }

def get_acceleration_summary(session_data):
    """Get acceleration-related metrics summary."""
    if session_data.empty:
        return {
            'ACC': 0.0,
            'DEC': 0.0,
            'ACC_Rel': 0.0,
            'DEC_Rel': 0.0
        }
    
    return {
        'ACC': float(session_data['ACC'].max()),
        'DEC': float(session_data['DEC'].min()),
        'ACC_Rel': float(session_data['ACC_Rel'].mean()),
        'DEC_Rel': float(session_data['DEC_Rel'].mean())
    }