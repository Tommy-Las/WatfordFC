import pandas as pd
import plotly.graph_objects as go
from datetime import timedelta
from functions.data_processing import format_date_microcycle

# Define color scheme
COLORS = {
    'primary': '#FFD700',    # Yellow
    'secondary': '#FF4B4B',  # Red
    'background': 'white',   # White background
    'text': 'black',         # Black text
    'max_line': 'black'      # Black line for max values
}

def plot_speed_timeline(df, player_name, selected_date, selected_microcycle):
    """Create speed timeline visualization."""
    selected_date = pd.to_datetime(selected_date)
    start_date = selected_date - timedelta(days=7)
    
    timeline_data = df[
        (df['PlayerID'] == player_name) & 
        (df['DATE'] >= start_date) & 
        (df['DATE'] <= selected_date)
    ].copy()
    
    timeline_data = timeline_data.sort_values('DATE')
    timeline_data['is_selected'] = (
        (timeline_data['DATE'].dt.date == selected_date.date()) & 
        (timeline_data['Microcycle'] == selected_microcycle)
    )
    
    timeline_data['date_label'] = timeline_data.apply(
        lambda x: format_date_microcycle(x['DATE'], x['Microcycle']), axis=1
    )
    
    all_time_max = timeline_data['Max Speed Season'].iloc[0]
    
    fig = go.Figure()
    
    # Add continuous line for all sessions
    fig.add_trace(go.Scatter(
        x=timeline_data['date_label'],
        y=timeline_data['Max Speed'],
        name='Max Speed',
        line=dict(color=COLORS['primary']),
        mode='lines+markers'
    ))
    
    # Add star marker for selected session
    selected = timeline_data[timeline_data['is_selected']]
    if not selected.empty:
        fig.add_trace(go.Scatter(
            x=selected['date_label'],
            y=selected['Max Speed'],
            name='Selected Session',
            mode='markers',
            marker=dict(color=COLORS['secondary'], size=12, symbol='star'),
            showlegend=True
        ))
    
    fig.add_hline(
        y=all_time_max,
        line_dash="dash",
        line_color=COLORS['max_line'],
        annotation_text=f"Season Max: {all_time_max:.1f} km/h",
        annotation_position="top right"
    )
    
    fig.update_layout(
        title='Speed Timeline',
        xaxis_title='Session',
        yaxis_title='Speed (km/h)',
        showlegend=True,
        hovermode='x unified',
        xaxis=dict(tickangle=45),
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text'])
    )
    
    return fig

def plot_acceleration_timeline(df, player_name, selected_date, selected_microcycle):
    """Create acceleration/deceleration timeline visualization."""
    selected_date = pd.to_datetime(selected_date)
    start_date = selected_date - timedelta(days=7)
    
    timeline_data = df[
        (df['PlayerID'] == player_name) & 
        (df['DATE'] >= start_date) & 
        (df['DATE'] <= selected_date)
    ].copy()
    
    timeline_data = timeline_data.sort_values('DATE')
    timeline_data['is_selected'] = (
        (timeline_data['DATE'].dt.date == selected_date.date()) & 
        (timeline_data['Microcycle'] == selected_microcycle)
    )
    
    timeline_data['date_label'] = timeline_data.apply(
        lambda x: format_date_microcycle(x['DATE'], x['Microcycle']), axis=1
    )
    
    fig = go.Figure()
    
    # Add continuous lines for acceleration and deceleration
    fig.add_trace(go.Scatter(
        x=timeline_data['date_label'],
        y=timeline_data['ACC'],
        name='Max Acceleration',
        line=dict(color=COLORS['primary']),
        mode='lines+markers'
    ))
    
    fig.add_trace(go.Scatter(
        x=timeline_data['date_label'],
        y=timeline_data['DEC'],
        name='Max Deceleration',
        line=dict(color=COLORS['secondary']),
        mode='lines+markers'
    ))
    
    # Add star markers for selected session
    selected = timeline_data[timeline_data['is_selected']]
    if not selected.empty:
        fig.add_trace(go.Scatter(
            x=selected['date_label'],
            y=selected['ACC'],
            name='Selected Session (Accel)',
            mode='markers',
            marker=dict(color=COLORS['primary'], size=12, symbol='star'),
            showlegend=True
        ))
        fig.add_trace(go.Scatter(
            x=selected['date_label'],
            y=selected['DEC'],
            name='Selected Session (Decel)',
            mode='markers',
            marker=dict(color=COLORS['secondary'], size=12, symbol='star'),
            showlegend=True
        ))
    
    fig.update_layout(
        title='Acceleration Timeline',
        xaxis_title='Session',
        yaxis_title='Acceleration (m/s²)',
        showlegend=True,
        hovermode='x unified',
        xaxis=dict(tickangle=45),
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text'])
    )
    
    return fig

def plot_distance_timeline(df, player_name, selected_date, selected_microcycle):
    """Create distance timeline visualization."""
    selected_date = pd.to_datetime(selected_date)
    start_date = selected_date - timedelta(days=7)
    
    timeline_data = df[
        (df['PlayerID'] == player_name) & 
        (df['DATE'] >= start_date) & 
        (df['DATE'] <= selected_date)
    ].copy()
    
    timeline_data = timeline_data.sort_values('DATE')
    timeline_data['is_selected'] = (
        (timeline_data['DATE'].dt.date == selected_date.date()) & 
        (timeline_data['Microcycle'] == selected_microcycle)
    )
    
    timeline_data['date_label'] = timeline_data.apply(
        lambda x: format_date_microcycle(x['DATE'], x['Microcycle']), axis=1
    )
    
    all_time_max = timeline_data['TD'].max()
    
    fig = go.Figure()
    
    # Add continuous line for all sessions
    fig.add_trace(go.Scatter(
        x=timeline_data['date_label'],
        y=timeline_data['TD'],
        name='Total Distance',
        line=dict(color=COLORS['primary']),
        mode='lines+markers'
    ))
    
    # Add star marker for selected session
    selected = timeline_data[timeline_data['is_selected']]
    if not selected.empty:
        fig.add_trace(go.Scatter(
            x=selected['date_label'],
            y=selected['TD'],
            name='Selected Session',
            mode='markers',
            marker=dict(color=COLORS['secondary'], size=12, symbol='star'),
            showlegend=True
        ))
    
    fig.add_hline(
        y=all_time_max,
        line_dash="dash",
        line_color=COLORS['max_line'],
        annotation_text=f"All-time Max: {all_time_max:.0f} m",
        annotation_position="top right"
    )
    
    fig.update_layout(
        title='Distance Timeline',
        xaxis_title='Session',
        yaxis_title='Distance (m)',
        showlegend=True,
        hovermode='x unified',
        xaxis=dict(tickangle=45),
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text'])
    )
    
    return fig

def plot_performance_timeline(df, player_name, selected_date, selected_microcycle):
    """Create performance (sprints) timeline visualization."""
    selected_date = pd.to_datetime(selected_date)
    start_date = selected_date - timedelta(days=7)
    
    timeline_data = df[
        (df['PlayerID'] == player_name) & 
        (df['DATE'] >= start_date) & 
        (df['DATE'] <= selected_date)
    ].copy()
    
    timeline_data = timeline_data.sort_values('DATE')
    timeline_data['is_selected'] = (
        (timeline_data['DATE'].dt.date == selected_date.date()) & 
        (timeline_data['Microcycle'] == selected_microcycle)
    )
    
    timeline_data['date_label'] = timeline_data.apply(
        lambda x: format_date_microcycle(x['DATE'], x['Microcycle']), axis=1
    )
    
    all_time_max = timeline_data['Sprints'].max()
    
    fig = go.Figure()
    
    # Add continuous line for all sessions
    fig.add_trace(go.Scatter(
        x=timeline_data['date_label'],
        y=timeline_data['Sprints'],
        name='Total Sprints',
        line=dict(color=COLORS['primary']),
        mode='lines+markers'
    ))
    
    # Add star marker for selected session
    selected = timeline_data[timeline_data['is_selected']]
    if not selected.empty:
        fig.add_trace(go.Scatter(
            x=selected['date_label'],
            y=selected['Sprints'],
            name='Selected Session',
            mode='markers',
            marker=dict(color=COLORS['secondary'], size=12, symbol='star'),
            showlegend=True
        ))
    
    fig.add_hline(
        y=all_time_max,
        line_dash="dash",
        line_color=COLORS['max_line'],
        annotation_text=f"All-time Max: {all_time_max} sprints",
        annotation_position="top right"
    )
    
    fig.update_layout(
        title='Sprints Timeline',
        xaxis_title='Session',
        yaxis_title='Number of Sprints',
        showlegend=True,
        hovermode='x unified',
        xaxis=dict(tickangle=45),
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text'])
    )
    
    return fig

def classify_player(df, player_name):
    """Classify player based on their performance metrics."""
    player_data = df[df['PlayerID'] == player_name]
    
    # Calculate z-scores for key metrics
    speed_zscore = (player_data['Max Speed'].mean() - df['Max Speed'].mean()) / df['Max Speed'].std()
    distance_zscore = (player_data['TD'].mean() - df['TD'].mean()) / df['TD'].std()
    
    if speed_zscore > 1:
        return "High Intensity"
    elif distance_zscore > 1:
        return "High Distance"
    else:
        return "Balanced Performance"