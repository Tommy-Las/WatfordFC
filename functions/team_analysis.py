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

"""
Calculate aggregated team metrics with optional date/microcycle filter.
"""
def calculate_team_metrics(df, selected_date=None, selected_microcycle=None):
    
    metrics_df = df.copy()
    
    if selected_date and selected_microcycle:
        
        # Filter for selected session metrics
        session_metrics = metrics_df[
            (metrics_df['DATE'].dt.date == selected_date) & 
            (metrics_df['Microcycle'] == selected_microcycle)
        ]
        
        # Return team session metrics grouped by date and microcycle
        if not session_metrics.empty:
            return session_metrics.groupby(['DATE', 'Microcycle']).agg({
                'TD': 'mean',
                'Max Speed': 'mean',
                'Avg Speed Season': 'mean',
                'Sprints': 'sum',
                'Mins': 'sum',
                'ACC': 'max',
                'DEC': 'min',
                'HSR': 'mean',
                '+25 Km/h': 'mean'
            }).reset_index()
    
    # Calculate metrics for all sessions
    return metrics_df.groupby(['DATE', 'Microcycle']).agg({
        'TD': 'mean',
        'Max Speed': 'mean',
        'Avg Speed Season': 'mean',
        'Sprints': 'sum',
        'Mins': 'sum',
        'ACC': 'max',
        'DEC': 'min',
        'HSR': 'mean',
        '+25 Km/h': 'mean'
    }).reset_index()


"""
Create visualizations for team metrics showing timeline for last 7 days.
"""
def plot_team_metrics(team_metrics, selected_date=None):
    
    if selected_date is None:
        selected_date = team_metrics['DATE'].max()
    else:
        selected_date = pd.to_datetime(selected_date)
    
    # Filter data for last 7 days from selected date
    start_date = selected_date - timedelta(days=7)
    timeline_data = team_metrics[
        (team_metrics['DATE'] >= start_date) & 
        (team_metrics['DATE'] <= selected_date)
    ].sort_values('DATE')
    
    # Format dates for display
    timeline_data['date_label'] = timeline_data.apply(
        lambda x: format_date_microcycle(x['DATE'], x['Microcycle']), axis=1
    )
    
    # Team distance timeline
    fig_team_distance = go.Figure()
    
    # Add distance line
    fig_team_distance.add_trace(go.Scatter(
        x=timeline_data['date_label'],
        y=timeline_data['TD'],
        name='Average Distance',
        line=dict(color=COLORS['primary']),
        mode='lines+markers'
    ))
    
    # Add all-time max reference line
    all_time_max_distance = timeline_data['TD'].max()
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
        y=timeline_data['Sprints'],
        name='Total Sprints',
        line=dict(color=COLORS['primary']),
        mode='lines+markers'
    ))
    
    # Add HSR line
    fig_team_sprints.add_trace(go.Scatter(
        x=timeline_data['date_label'],
        y=timeline_data['HSR'],
        name='High Speed Running (+19 km/h)',
        line=dict(color=COLORS['secondary']),
        mode='lines+markers'
    ))
    
    # Add +25 km/h line
    fig_team_sprints.add_trace(go.Scatter(
        x=timeline_data['date_label'],
        y=timeline_data['+25 Km/h'],
        name='Very High Speed Running (+25 km/h)',
        line=dict(color='#4B0082'),  # Deep purple color
        mode='lines+markers'
    ))
    
    fig_team_sprints.update_layout(
        title='Team High Intensity Actions (Last 7 Days)',
        xaxis_title='Session',
        yaxis_title='Count',
        hovermode='x unified',
        xaxis=dict(tickangle=45),
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text'])
    )
    
    return fig_team_distance, fig_team_sprints