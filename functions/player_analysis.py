import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

def load_player_data(data_path):
    """Load and prepare player GPS data."""
    df = pd.read_csv(data_path)
    return df

def calculate_relative_metrics(df, player_id):
    """Calculate relative metrics for a player."""
    player_max_speed = df[df['player_id'] == player_id]['max_speed'].max()
    df.loc[df['player_id'] == player_id, 'relative_speed'] = (df[df['player_id'] == player_id]['max_speed'] / player_max_speed) * 100
    return df

def calculate_rolling_metrics(df, player_id, window):
    """Calculate rolling averages for specified window."""
    player_df = df[df['player_id'] == player_id].sort_values('date')
    player_df['rolling_distance'] = player_df['distance'].rolling(window=window).mean()
    player_df['rolling_max_speed'] = player_df['max_speed'].rolling(window=window).mean()
    return player_df

def classify_player(df, player_id):
    """Classify player based on their performance metrics."""
    player_stats = df[df['player_id'] == player_id].mean()
    
    if player_stats['max_speed'] > df['max_speed'].mean() + df['max_speed'].std():
        return "High Intensity Player"
    elif player_stats['distance'] > df['distance'].mean() + df['distance'].std():
        return "High Distance Player"
    else:
        return "Balanced Performance Player"

def plot_player_metrics(df, player_id):
    """Create visualizations for player metrics."""
    player_df = df[df['player_id'] == player_id]
    
    # Speed over time
    fig_speed = px.line(player_df, x='date', y=['max_speed', 'avg_speed'],
                        title='Speed Metrics Over Time')
    
    # Distance by microcycle
    fig_distance = px.bar(player_df, x='date', y='distance',
                         color='microcycle',
                         title='Distance by Date and Microcycle')
    
    return fig_speed, fig_distance