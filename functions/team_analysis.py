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

def plot_team_metrics(team_metrics, selected_date=None):
    """Create visualizations for team metrics showing timeline for last 7 days."""
    if selected_date is None:
        selected_date = team_metrics['date'].max()
    else:
        selected_date = pd.to_datetime(selected_date)
    
    # Filter data for last 7 days from selected date
    start_date = selected_date - timedelta(days=7)
    timeline_data = team_metrics[
        (team_metrics['date'] >= start_date) & 
        (team_metrics['date'] <= selected_date)
    ].sort_values('date')
    
    # Format dates for display
    timeline_data['date_label'] = timeline_data.apply(
        lambda x: format_date_microcycle(x['date'], x['microcycle']), axis=1
    )
    
    # Team distance timeline
    fig_team_distance = go.Figure()
    
    # Add distance line
    fig_team_distance.add_trace(go.Scatter(
        x=timeline_data['date_label'],
        y=timeline_data['distance'],
        name='Average Distance',
        line=dict(color=COLORS['primary']),
        mode='lines+markers'
    ))
    
    # Add all-time max reference line
    all_time_max_distance = timeline_data['distance'].max()
    fig_team_distance.add_hline(
        y=all_time_max_distance,
        line_dash="dash",
        line_color=COLORS['max_line'],
        annotation_text=f"All-time Max: {all_time_max_distance:.0f} m",
        annotation_position="top right"
    )
    
    fig_team_distance.update_layout(
        title='Team Average Distance (Last 7 Days)',
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
    
    # Add sprints line
    fig_team_sprints.add_trace(go.Scatter(
        x=timeline_data['date_label'],
        y=timeline_data['total_sprints'],
        name='Total Sprints',
        line=dict(color=COLORS['primary']),
        mode='lines+markers'
    ))
    
    # Add all-time max reference line
    all_time_max_sprints = timeline_data['total_sprints'].max()
    fig_team_sprints.add_hline(
        y=all_time_max_sprints,
        line_dash="dash",
        line_color=COLORS['max_line'],
        annotation_text=f"All-time Max: {all_time_max_sprints:.0f} sprints",
        annotation_position="top right"
    )
    
    fig_team_sprints.update_layout(
        title='Total Team Sprints (Last 7 Days)',
        xaxis_title='Session',
        yaxis_title='Total Sprints',
        hovermode='x unified',
        xaxis=dict(tickangle=45),
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text'])
    )
    
    return fig_team_distance, fig_team_sprints