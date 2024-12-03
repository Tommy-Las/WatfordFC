import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import timedelta

# Define color scheme
COLORS = {
    'primary': '#FFD700',    # Yellow
    'secondary': '#FF4B4B',  # Red
    'background': 'white',   # White background
    'text': 'black',         # Black text
    'max_line': 'black'      # Black line for max speed
}

def format_date_microcycle(date, microcycle):
    """Format date and microcycle in the desired format."""
    return f"{date.strftime('%B %d')} - {microcycle}"

def get_player_max_speed(df, player_id):
    """Get the all-time maximum speed for a player."""
    return df[df['player_id'] == player_id]['max_speed'].max()

def plot_speed_acceleration_profile(df, player_id, selected_date, selected_microcycle):
    """Create speed and acceleration visualizations for player with 7-day timeline."""
    selected_date = pd.to_datetime(selected_date)
    start_date = selected_date - timedelta(days=7)
    end_date = selected_date
    
    timeline_data = df[
        (df['player_id'] == player_id) & 
        (df['date'] >= start_date) & 
        (df['date'] <= end_date)
    ].sort_values('date')
    
    timeline_data['date_label'] = timeline_data.apply(
        lambda x: format_date_microcycle(x['date'], x['microcycle']), axis=1
    )
    
    all_time_max = get_player_max_speed(df, player_id)
    
    # Speed profile
    fig_speed = go.Figure()
    
    fig_speed.add_trace(go.Scatter(
        x=timeline_data['date_label'],
        y=timeline_data['max_speed'],
        name='Max Speed',
        line=dict(color=COLORS['primary']),
        mode='lines+markers'
    ))
    
    fig_speed.add_trace(go.Scatter(
        x=timeline_data['date_label'],
        y=timeline_data['avg_speed'],
        name='Avg Speed',
        line=dict(color=COLORS['secondary'], dash='dot'),
        mode='lines+markers'
    ))
    
    fig_speed.add_hline(
        y=all_time_max,
        line_dash="dash",
        line_color=COLORS['max_line'],
        annotation_text=f"All-time Max: {all_time_max:.1f} km/h",
        annotation_position="top right"
    )
    
    selected_session = timeline_data[timeline_data['microcycle'] == selected_microcycle]
    if not selected_session.empty:
        fig_speed.add_trace(go.Scatter(
            x=selected_session['date_label'],
            y=selected_session['max_speed'],
            name='Selected Session',
            mode='markers',
            marker=dict(color=COLORS['secondary'], size=12, symbol='star'),
            showlegend=True
        ))
    
    fig_speed.update_layout(
        title='Speed Profile (Last 7 Days)',
        xaxis_title='Date',
        yaxis_title='Speed (km/h)',
        showlegend=True,
        hovermode='x unified',
        xaxis=dict(tickangle=45),
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text'])
    )
    
    # Acceleration profile
    fig_accel = go.Figure()
    
    fig_accel.add_trace(go.Scatter(
        x=timeline_data['date_label'],
        y=timeline_data['max_acceleration'],
        name='Max Acceleration',
        line=dict(color=COLORS['primary']),
        mode='lines+markers'
    ))
    
    fig_accel.add_trace(go.Scatter(
        x=timeline_data['date_label'],
        y=timeline_data['max_deceleration'],
        name='Max Deceleration',
        line=dict(color=COLORS['secondary']),
        mode='lines+markers'
    ))
    
    if not selected_session.empty:
        fig_accel.add_trace(go.Scatter(
            x=selected_session['date_label'],
            y=selected_session['max_acceleration'],
            name='Selected Session (Accel)',
            mode='markers',
            marker=dict(color=COLORS['primary'], size=12, symbol='star'),
            showlegend=True
        ))
        fig_accel.add_trace(go.Scatter(
            x=selected_session['date_label'],
            y=selected_session['max_deceleration'],
            name='Selected Session (Decel)',
            mode='markers',
            marker=dict(color=COLORS['secondary'], size=12, symbol='star'),
            showlegend=True
        ))
    
    fig_accel.update_layout(
        title='Acceleration Profile (Last 7 Days)',
        xaxis_title='Date',
        yaxis_title='Acceleration (m/s²)',
        showlegend=True,
        hovermode='x unified',
        xaxis=dict(tickangle=45),
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text'])
    )
    
    return fig_speed, fig_accel

def classify_player(df, player_id):
    """Classify player based on their performance metrics."""
    numeric_cols = ['max_speed', 'avg_speed', 'distance', 'max_acceleration', 
                   'max_deceleration', 'total_sprints', 'minutes']
    
    player_stats = df[df['player_id'] == player_id][numeric_cols].mean()
    team_stats = df[numeric_cols].mean()
    team_std = df[numeric_cols].std()
    
    speed_zscore = (player_stats['max_speed'] - team_stats['max_speed']) / team_std['max_speed']
    distance_zscore = (player_stats['distance'] - team_stats['distance']) / team_std['distance']
    
    if speed_zscore > 1:
        return "High Intensity Player"
    elif distance_zscore > 1:
        return "High Distance Player"
    else:
        return "Balanced Performance Player"

def get_session_summary(df, player_id, date, microcycle):
    """Get summary metrics for a specific session."""
    session_data = df[
        (df['date'].dt.date == date) & 
        (df['microcycle'] == microcycle) &
        (df['player_id'] == player_id)
    ]
    
    if session_data.empty:
        return None
    
    return {
        'max_speed': session_data['max_speed'].max(),
        'avg_speed': session_data['avg_speed'].mean(),
        'total_distance': session_data['distance'].sum(),
        'max_acceleration': session_data['max_acceleration'].max(),
        'max_deceleration': session_data['max_deceleration'].min(),
        'total_sprints': session_data['total_sprints'].sum(),
        'minutes': session_data['minutes'].max()
    }