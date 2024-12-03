import pandas as pd
import plotly.graph_objects as go
from datetime import timedelta

# Define color scheme
COLORS = {
    'primary': '#FFD700',    # Yellow
    'secondary': '#FF4B4B',  # Red
    'background': 'white',   # White background
    'text': 'black',         # Black text
    'max_line': 'black'      # Black line for max speed
}

def calculate_team_metrics(df, selected_date=None, selected_microcycle=None):
    """Calculate aggregated team metrics with optional date/microcycle filter."""
    metrics_df = df.copy()
    
    if selected_date and selected_microcycle:
        # Filter for selected session metrics
        session_metrics = metrics_df[
            (metrics_df['date'].dt.date == selected_date) & 
            (metrics_df['microcycle'] == selected_microcycle)
        ]
        
        if not session_metrics.empty:
            return session_metrics.groupby(['date', 'microcycle']).agg({
                'distance': 'mean',
                'max_speed': 'mean',
                'avg_speed': 'mean',
                'total_sprints': 'sum',
                'minutes': 'sum',
                'max_acceleration': 'max',
                'max_deceleration': 'min'
            }).reset_index()
    
    # Calculate metrics for all sessions
    return metrics_df.groupby(['date', 'microcycle']).agg({
        'distance': 'mean',
        'max_speed': 'mean',
        'avg_speed': 'mean',
        'total_sprints': 'sum',
        'minutes': 'sum',
        'max_acceleration': 'max',
        'max_deceleration': 'min'
    }).reset_index()

def plot_team_metrics(team_metrics):
    """Create visualizations for team metrics showing timeline."""
    # Sort data by date
    team_metrics = team_metrics.sort_values('date')
    
    # Format dates for display
    team_metrics['date_label'] = team_metrics.apply(
        lambda x: f"{x['date'].strftime('%B %d')} - {x['microcycle']}", axis=1
    )
    
    # Team distance over time
    fig_team_distance = go.Figure()
    
    fig_team_distance.add_trace(go.Scatter(
        x=team_metrics['date_label'],
        y=team_metrics['distance'],
        mode='lines+markers',
        name='Average Distance',
        line=dict(color=COLORS['primary'])
    ))
    
    fig_team_distance.update_layout(
        title='Team Average Distance Timeline',
        xaxis_title='Session',
        yaxis_title='Average Distance (m)',
        hovermode='x unified',
        xaxis=dict(tickangle=45),
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text'])
    )
    
    # Team sprints timeline
    fig_team_sprints = go.Figure()
    
    fig_team_sprints.add_trace(go.Bar(
        x=team_metrics['date_label'],
        y=team_metrics['total_sprints'],
        marker_color=COLORS['secondary']
    ))
    
    fig_team_sprints.update_layout(
        title='Total Team Sprints Timeline',
        xaxis_title='Session',
        yaxis_title='Total Sprints',
        bargap=0.2,
        xaxis=dict(tickangle=45),
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text'])
    )
    
    return fig_team_distance, fig_team_sprints