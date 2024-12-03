import pandas as pd
import numpy as np

def calculate_injury_prevention_index(session_data):
    """Calculate injury prevention index (placeholder)."""
    if session_data.empty:
        return 0
    
    # Placeholder implementation
    # TODO: Implement actual injury prevention calculation logic
    return 0

def get_performance_summary(session_data):
    """Get general performance metrics summary."""
    if session_data.empty:
        return {
            'total_sprints': 0,
            'minutes': 0,
            'injury_prevention_index': 0
        }
    
    return {
        'total_sprints': int(session_data['total_sprints'].sum()),
        'minutes': int(session_data['minutes'].max()),
        'injury_prevention_index': calculate_injury_prevention_index(session_data)
    }