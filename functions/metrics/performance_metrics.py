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
            'Sprints': 0,
            'Mins': 0,
            'injury_prevention_index': 0
        }
    
    return {
        'Sprints': int(session_data['Sprints'].sum()),
        'Mins': int(session_data['Mins'].max()),
        'injury_prevention_index': calculate_injury_prevention_index(session_data)
    }