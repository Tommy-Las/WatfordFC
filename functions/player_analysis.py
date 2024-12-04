import pandas as pd
import plotly.graph_objects as go
from datetime import timedelta

# Define color scheme
COLORS = {
    'primary': '#FFD700',    # Yellow
    'secondary': '#FF4B4B',  # Red
    'background': 'white',   # White background
    'text': 'black',         # Black text
    'max_line': 'black'      # Black line for max values
}

def format_date_microcycle(date, microcycle):
    """Format date and microcycle in the desired format."""
    return f"{date.strftime('%Y %B %d')} - {microcycle}"

def plot_speed_timeline(df, player_name, selected_date, selected_microcycle):
    """Create speed timeline visualization."""
    selected_date = pd.to_datetime(selected_date)
    start_date = selected_date - timedelta(days=7)
    
    timeline_data = df[
        (df['PlayerID'] == player_name) & 
        (df['DATE'] >= start_date) & 
        (df['DATE'] <= selected_date)
    ].sort_values('DATE')
    
    timeline_data['date_label'] = timeline_data.apply(
        lambda x: format_date_microcycle(x['DATE'], x['Microcycle']), axis=1
    )
    
    all_time_max = timeline_data['Max Speed'].max()
    
    fig = go.Figure()
    
    # Add max speed line
    fig.add_trace(go.Scatter(
        x=timeline_data['date_label'],
        y=timeline_data['Max Speed'],
        name='Max Speed',
        line=dict(color=COLORS['primary']),
        mode='lines+markers'
    ))
    
    # Add all-time max reference line
    fig.add_hline(
        y=all_time_max,
        line_dash="dash",
        line_color=COLORS['max_line'],
        annotation_text=f"All-time Max: {all_time_max:.1f} km/h",
        annotation_position="top right"
    )
    
    # Highlight selected session
    selected_session = timeline_data[timeline_data['Microcycle'] == selected_microcycle]
    if not selected_session.empty:
        fig.add_trace(go.Scatter(
            x=selected_session['date_label'],
            y=selected_session['Max Speed'],
            name='Selected Session',
            mode='markers',
            marker=dict(color=COLORS['secondary'], size=12, symbol='star')
        ))
    
    fig.update_layout(
        title='Speed Timeline (Last 7 Days)',
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
    ].sort_values('DATE')
    
    timeline_data['date_label'] = timeline_data.apply(
        lambda x: format_date_microcycle(x['DATE'], x['Microcycle']), axis=1
    )
    
    fig = go.Figure()
    
    # Add acceleration line
    fig.add_trace(go.Scatter(
        x=timeline_data['date_label'],
        y=timeline_data['ACC'],
        name='Max Acceleration',
        line=dict(color=COLORS['primary']),
        mode='lines+markers'
    ))
    
    # Add deceleration line
    fig.add_trace(go.Scatter(
        x=timeline_data['date_label'],
        y=timeline_data['DEC'],
        name='Max Deceleration',
        line=dict(color=COLORS['secondary']),
        mode='lines+markers'
    ))
    
    # Highlight selected session
    selected_session = timeline_data[timeline_data['Microcycle'] == selected_microcycle]
    if not selected_session.empty:
        fig.add_trace(go.Scatter(
            x=selected_session['date_label'],
            y=selected_session['ACC'],
            name='Selected Session (Accel)',
            mode='markers',
            marker=dict(color=COLORS['primary'], size=12, symbol='star')
        ))
        fig.add_trace(go.Scatter(
            x=selected_session['date_label'],
            y=selected_session['ACC'],
            name='Selected Session (Decel)',
            mode='markers',
            marker=dict(color=COLORS['secondary'], size=12, symbol='star')
        ))
    
    fig.update_layout(
        title='Acceleration Timeline (Last 7 Days)',
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
    ].sort_values('DATE')
    
    timeline_data['date_label'] = timeline_data.apply(
        lambda x: format_date_microcycle(x['DATE'], x['Microcycle']), axis=1
    )
    
    all_time_max = timeline_data['TD'].max()
    
    fig = go.Figure()
    
    # Add distance line
    fig.add_trace(go.Scatter(
        x=timeline_data['date_label'],
        y=timeline_data['TD'],
        name='Total Distance',
        line=dict(color=COLORS['primary']),
        mode='lines+markers'
    ))
    
    # Add all-time max reference line
    fig.add_hline(
        y=all_time_max,
        line_dash="dash",
        line_color=COLORS['max_line'],
        annotation_text=f"All-time Max: {all_time_max:.0f} m",
        annotation_position="top right"
    )
    
    # Highlight selected session
    selected_session = timeline_data[timeline_data['Microcycle'] == selected_microcycle]
    if not selected_session.empty:
        fig.add_trace(go.Scatter(
            x=selected_session['date_label'],
            y=selected_session['TD'],
            name='Selected Session',
            mode='markers',
            marker=dict(color=COLORS['secondary'], size=12, symbol='star')
        ))
    
    fig.update_layout(
        title='Distance Timeline (Last 7 Days)',
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
    ].sort_values('DATE')
    
    timeline_data['date_label'] = timeline_data.apply(
        lambda x: format_date_microcycle(x['DATE'], x['Microcycle']), axis=1
    )
    
    all_time_max = timeline_data['Sprints'].max()
    
    fig = go.Figure()
    
    # Add sprints line
    fig.add_trace(go.Scatter(
        x=timeline_data['date_label'],
        y=timeline_data['Sprints'],
        name='Total Sprints',
        line=dict(color=COLORS['primary']),
        mode='lines+markers'
    ))
    
    # Add all-time max reference line
    fig.add_hline(
        y=all_time_max,
        line_dash="dash",
        line_color=COLORS['max_line'],
        annotation_text=f"All-time Max: {all_time_max} sprints",
        annotation_position="top right"
    )
    
    # Highlight selected session
    selected_session = timeline_data[timeline_data['Microcycle'] == selected_microcycle]
    if not selected_session.empty:
        fig.add_trace(go.Scatter(
            x=selected_session['date_label'],
            y=selected_session['Sprints'],
            name='Selected Session',
            mode='markers',
            marker=dict(color=COLORS['secondary'], size=12, symbol='star')
        ))
    
    fig.update_layout(
        title='Sprints Timeline (Last 7 Days)',
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