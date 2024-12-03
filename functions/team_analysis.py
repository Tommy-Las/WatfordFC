import pandas as pd
import plotly.express as px
import streamlit as st

def calculate_team_metrics(df):
    """Calculate aggregated team metrics."""
    team_metrics = df.groupby(['date', 'microcycle']).agg({
        'distance': 'mean',
        'max_speed': 'mean',
        'total_sprints': 'sum',
        'minutes': 'sum'
    }).reset_index()
    return team_metrics

def plot_team_metrics(team_metrics):
    """Create visualizations for team metrics."""
    # Team distance over time
    fig_team_distance = px.line(team_metrics, x='date', y='distance',
                               title='Team Average Distance Over Time')
    
    # Team sprints by microcycle
    fig_team_sprints = px.bar(team_metrics, x='microcycle', y='total_sprints',
                             title='Total Team Sprints by Microcycle')
    
    return fig_team_distance, fig_team_sprints