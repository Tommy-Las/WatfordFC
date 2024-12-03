import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from common.session import check_password
from common.menu import show_menu
from functions.data_processing import (
    load_and_prepare_data,
    get_player_id_by_name
)
from functions.player_analysis import (
    plot_speed_acceleration_profile,
    classify_player
)
from functions.metrics.speed_metrics import calculate_relative_speed_metrics
from functions.metrics.acceleration_metrics import calculate_relative_acceleration_metrics
from functions.metrics.distance_metrics import calculate_relative_distance_metrics
from functions.metrics.performance_metrics import get_performance_summary
from functions.team_analysis import calculate_team_metrics, plot_team_metrics

# Page configuration
st.set_page_config(
    page_title="GPS Analysis Platform",
    page_icon="assets/logo.png",
    layout="wide"
)

st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #1E1E1E;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
    [data-testid="stSidebar"] .stRadio label,
    [data-testid="stSidebar"] .stTitle {
        color: white !important;
    }
    [data-testid="stSidebar"] button {
        background-color: #FFD700;
        color: black;
    }
    [data-testid="stSidebar"] button:hover {
        background-color: #ffdc1f;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Custom CSS for styling
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #262730;
        color: white;
    }
    .sidebar .widget-label {
        color: white !important;
    }
    .sidebar .stRadio > label {
        color: white !important;
    }
    .sidebar .stButton > button {
        color: white;
        background-color: #262730;
        border: 1px solid white;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    if not check_password():
        st.stop()
    
    # Load data
    df = load_and_prepare_data("data/sample_gps_data.csv")
    
    # Show menu
    choice = show_menu()
    
    if choice == "Player Analysis":
        st.title("Player Physical Profile Analysis")
        
        # Player selection
        player_name = st.selectbox("Select Player", sorted(df['player_name'].unique()))
        player_id = get_player_id_by_name(df, player_name)
        
        # Session selection
        session_options = df[['date', 'microcycle']].drop_duplicates()
        session_options['date_label'] = session_options.apply(
            lambda x: f"{x['date'].strftime('%B %d')} - {x['microcycle']}", axis=1
        )
        selected_session = st.selectbox(
            "Select Session",
            sorted(session_options['date_label'], reverse=True)
        )
        
        selected_date = session_options[
            session_options['date_label'] == selected_session
        ]['date'].iloc[0].date()
        selected_microcycle = session_options[
            session_options['date_label'] == selected_session
        ]['microcycle'].iloc[0]
        
        # Get session data
        session_data = df[
            (df['date'].dt.date == selected_date) & 
            (df['microcycle'] == selected_microcycle) &
            (df['player_id'] == player_id)
        ]
        
        if not session_data.empty:
            # Speed Metrics Section
            st.header("Speed Metrics") 
            speed_metrics = calculate_relative_speed_metrics(df, player_id, session_data)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Max Speed (km/h)", f"{speed_metrics['max_speed']:.1f}")
            with col2:
                st.metric("Relative Max Speed (%)", f"{speed_metrics['relative_max_speed']:.1f}")
            with col3:
                st.metric("Avg Speed (km/h)", f"{speed_metrics['avg_speed']:.1f}")
            with col4:
                st.metric("Relative Avg Speed (%)", f"{speed_metrics['relative_avg_speed']:.1f}")
            
            # Acceleration & Deceleration Metrics Section
            st.header("Acceleration & Deceleration Metrics")
            accel_metrics = calculate_relative_acceleration_metrics(df, player_id, session_data)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Max Acceleration (m/s²)", f"{accel_metrics['max_acceleration']:.1f}")
            with col2:
                st.metric("Relative Acceleration (%)", f"{accel_metrics['relative_acceleration']:.1f}")
            with col3:
                st.metric("Max Deceleration (m/s²)", f"{accel_metrics['max_deceleration']:.1f}")
            with col4:
                st.metric("Relative Deceleration (%)", f"{accel_metrics['relative_deceleration']:.1f}")
            
            # Distance Metrics Section
            st.header("Distance Metrics")
            distance_metrics = calculate_relative_distance_metrics(df, player_id, session_data)
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Distance (m)", f"{distance_metrics['total_distance']:.0f}")
            with col2:
                st.metric("Relative Distance (%)", f"{distance_metrics['relative_distance']:.1f}")
            
            # Performance Metrics Section
            st.header("Performance Metrics")
            perf_metrics = get_performance_summary(session_data)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Sprints", perf_metrics['total_sprints'])
            with col2:
                st.metric("Minutes", perf_metrics['minutes'])
            with col3:
                st.metric("Player Classification", classify_player(df, player_id))
            with col4:
                st.metric("Injury Prevention Index", perf_metrics['injury_prevention_index'])
            
            # Visualizations Section
            st.header("Performance Visualizations")
            fig_speed, fig_accel = plot_speed_acceleration_profile(
                df, player_id, selected_date, selected_microcycle
            )
            st.plotly_chart(fig_speed, use_container_width=True)
            st.plotly_chart(fig_accel, use_container_width=True)
            
    else:  # Team Analysis
        st.title("Team GPS Analysis")
        
        # Session selection (same as player analysis)
        session_options = df[['date', 'microcycle']].drop_duplicates()
        session_options['date_label'] = session_options.apply(
            lambda x: f"{x['date'].strftime('%B %d')} - {x['microcycle']}", axis=1
        )
        selected_session = st.selectbox(
            "Select Session",
            sorted(session_options['date_label'], reverse=True)
        )
        
        selected_date = session_options[
            session_options['date_label'] == selected_session
        ]['date'].iloc[0].date()
        selected_microcycle = session_options[
            session_options['date_label'] == selected_session
        ]['microcycle'].iloc[0]
        
        # Calculate team metrics
        team_metrics = calculate_team_metrics(df, selected_date, selected_microcycle)
        
        # Display team metrics
        st.header("Team Overview")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Average Distance (m)", f"{team_metrics['distance'].mean():.0f}")
        with col2:
            st.metric("Average Max Speed (km/h)", f"{team_metrics['max_speed'].mean():.1f}")
        with col3:
            st.metric("Total Team Sprints", f"{team_metrics['total_sprints'].sum():.0f}")
        with col4:
            st.metric("Total Team Minutes", f"{team_metrics['minutes'].sum():.0f}")
        
        # Team visualizations
        st.header("Team Performance Visualizations")
        all_team_metrics = calculate_team_metrics(df)
        fig_team_distance, fig_team_sprints = plot_team_metrics(all_team_metrics)
        st.plotly_chart(fig_team_distance, use_container_width=True)
        st.plotly_chart(fig_team_sprints, use_container_width=True)

if __name__ == "__main__":
    main()