import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Define color scheme
COLORS = {
    'primary': '#FFD700',    # Yellow
    'secondary': '#FF4B4B',  # Red
    'background': 'white',   # White background
    'text': 'black'         # Black text
}

def calculate_team_metrics(df):
    """Calculate aggregated team metrics."""
    team_metrics = df.groupby(['date', 'microcycle']).agg({
        'distance': 'mean',
        'max_speed': 'mean',
        'avg_speed': 'mean',
        'total_sprints': 'sum',
        'minutes': 'sum',
        'max_acceleration': 'max',
        'max_deceleration': 'min'
    }).reset_index()
    
    return team_metrics

def plot_team_metrics(team_metrics):
    """Create visualizations for team metrics."""
    team_metrics['date_formatted'] = team_metrics['date'].dt.strftime('%Y-%m-%d')
    
    # Team distance over time
    fig_team_distance = go.Figure()
    
    fig_team_distance.add_trace(go.Scatter(
        x=team_metrics['date_formatted'],
        y=team_metrics['distance'],
        mode='lines+markers',
        name='Average Distance',
        line=dict(color=COLORS['primary'])
    ))
    
    fig_team_distance.update_layout(
        title='Team Average Distance by Session',
        xaxis_title='Date',
        yaxis_title='Average Distance (m)',
        hovermode='x unified',
        xaxis=dict(tickangle=45),
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text'])
    )
    
    # Team sprints by microcycle
    fig_team_sprints = go.Figure()
    
    fig_team_sprints.add_trace(go.Bar(
        x=team_metrics['microcycle'],
        y=team_metrics['total_sprints'],
        marker_color=COLORS['secondary']
    ))
    
    fig_team_sprints.update_layout(
        title='Total Team Sprints by Session Type',
        xaxis_title='Session Type',
        yaxis_title='Total Sprints',
        bargap=0.2,
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text'])
    )
    
    return fig_team_distance, fig_team_sprints

def get_team_summary_metrics(team_metrics):
    """Calculate summary metrics for team dashboard."""
    return {
        'avg_distance': team_metrics['distance'].mean(),
        'total_minutes': team_metrics['minutes'].sum(),
        'avg_sprints': team_metrics['total_sprints'].mean(),
        'avg_max_speed': team_metrics['max_speed'].mean()
    }