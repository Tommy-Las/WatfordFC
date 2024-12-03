import streamlit as st
import pandas as pd
from datetime import datetime
from common.session import check_password
from common.menu import show_menu
from functions.data_processing import load_and_prepare_data, get_player_id_by_name
from functions.player_analysis import (
    plot_speed_acceleration_profile,
    classify_player,
    get_session_summary,
    format_date_microcycle
)
from functions.team_analysis import (
    calculate_team_metrics,
    plot_team_metrics,
    get_team_summary_metrics
)

# Custom theme configuration
st.set_page_config(
    page_title="GPS Analysis Platform",
    page_icon="assets/favicon.ico",
    layout="wide"
)

# Custom CSS for styling
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

def main():
    if not check_password():
        st.stop()
    
    # Load data
    df = load_and_prepare_data("data/sample_gps_data.csv")
    
    # Show menu
    choice = show_menu()
    
    if choice == "Player Analysis":
        st.title("Player Physical Profile Analysis")
        
        # Player selection by name
        player_name = st.selectbox("Select Player", sorted(df['player_name'].unique()))
        player_id = get_player_id_by_name(df, player_name)
        
        # Combined date and microcycle selection with formatted display
        date_microcycle_options = (df[['date', 'microcycle']]
            .drop_duplicates()
            .sort_values('date', ascending=True)
            .apply(
                lambda x: (x['date'], x['microcycle'], format_date_microcycle(x['date'], x['microcycle'])),
                axis=1
            ).tolist())
        
        selected_option = st.selectbox(
            "Select Session",
            date_microcycle_options,
            format_func=lambda x: x[2]
        )
        
        selected_date = selected_option[0].date()
        selected_microcycle = selected_option[1]
        
        # Get session summary
        summary = get_session_summary(df, player_id, selected_date, selected_microcycle)
        
        if summary:
            # Display metrics in two rows
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Max Speed (km/h)", f"{summary['max_speed']:.1f}")
            with col2:
                st.metric("Avg Speed (km/h)", f"{summary['avg_speed']:.1f}")
            with col3:
                st.metric("Total Distance (m)", f"{summary['total_distance']:.0f}")
            with col4:
                st.metric("Total Sprints", f"{summary['total_sprints']}")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Max Acceleration (m/s²)", f"{summary['max_acceleration']:.1f}")
            with col2:
                st.metric("Max Deceleration (m/s²)", f"{summary['max_deceleration']:.1f}")
            with col3:
                st.metric("Minutes", f"{summary['minutes']}")
            with col4:
                st.metric("Player Classification", classify_player(df, player_id))
            
            # Display plots
            fig_speed, fig_accel = plot_speed_acceleration_profile(
                df, player_id, selected_date, selected_microcycle
            )
            st.plotly_chart(fig_speed, use_container_width=True)
            st.plotly_chart(fig_accel, use_container_width=True)
        else:
            st.warning("No data available for the selected session.")
        
    else:  # Team Analysis
        st.title("Team GPS Analysis")
        
        # Calculate team metrics
        team_metrics = calculate_team_metrics(df)
        summary_metrics = get_team_summary_metrics(team_metrics)
        
        # Display team metrics
        st.subheader("Team Overview")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Avg Team Distance (m)", f"{summary_metrics['avg_distance']:.0f}")
        with col2:
            st.metric("Total Team Minutes", f"{summary_metrics['total_minutes']:.0f}")
        with col3:
            st.metric("Avg Team Sprints", f"{summary_metrics['avg_sprints']:.1f}")
        with col4:
            st.metric("Avg Max Speed (km/h)", f"{summary_metrics['avg_max_speed']:.2f}")
        
        # Display team plots
        fig_team_distance, fig_team_sprints = plot_team_metrics(team_metrics)
        st.plotly_chart(fig_team_distance, use_container_width=True)
        st.plotly_chart(fig_team_sprints, use_container_width=True)

if __name__ == "__main__":
    main()