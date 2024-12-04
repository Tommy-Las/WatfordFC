import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from common.session import check_password
from common.menu import show_menu
from functions.data_processing import load_and_prepare_data, get_player_id_by_name
from functions.player_analysis import (
    plot_speed_timeline,
    plot_acceleration_timeline,
    plot_distance_timeline,
    plot_performance_timeline,
    classify_player
)
from functions.metrics.speed_metrics import get_speed_metrics
from functions.metrics.acceleration_metrics import get_acceleration_metrics
from functions.metrics.distance_metrics import get_distance_metrics
from functions.metrics.performance_metrics import get_performance_summary
from functions.team_analysis import calculate_team_metrics, plot_team_metrics

# Page configuration
st.set_page_config(page_title="GPS Analysis Platform", layout="wide", page_icon='assets/logo.png')

# Load custom CSS
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def render_speed_tab(df, player_name, session_data, selected_date, selected_microcycle):
    """Render speed metrics tab content."""
    speed_metrics = get_speed_metrics(df, player_name, session_data)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Max Speed (km/h)", f"{speed_metrics['Max Speed']:.1f}")
    with col2:
        st.metric("Relative Max Speed (%)", f"{speed_metrics['% Max Speed']:.1f}")
    with col3:
        st.metric("Avg Speed (km/h)", f"{speed_metrics['Avg Speed Season']:.1f}")
    with col4:
        st.metric("Season Max Speed (km/h)", f"{speed_metrics['Max Speed Season']:.1f}")
    
    st.plotly_chart(
        plot_speed_timeline(df, player_name, selected_date, selected_microcycle),
        use_container_width=True
    )

def render_acceleration_tab(df, player_name, session_data, selected_date, selected_microcycle):
    """Render acceleration metrics tab content."""
    accel_metrics = get_acceleration_metrics(df, player_name, session_data)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Max Acceleration (m/s²)", f"{accel_metrics['ACC']:.1f}")
    with col2:
        st.metric("Relative Acceleration (%)", f"{accel_metrics['ACC_Rel']:.1f}")
    with col3:
        st.metric("Max Deceleration (m/s²)", f"{accel_metrics['DEC']:.1f}")
    with col4:
        st.metric("Relative Deceleration (%)", f"{accel_metrics['DEC_Rel']:.1f}")
    
    st.plotly_chart(
        plot_acceleration_timeline(df, player_name, selected_date, selected_microcycle),
        use_container_width=True
    )

def render_distance_tab(df, player_name, session_data, selected_date, selected_microcycle):
    """Render distance metrics tab content."""
    distance_metrics = get_distance_metrics(df, player_name, session_data)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Distance (m)", f"{distance_metrics['TD']:.0f}")
    with col2:
        st.metric("Relative Distance (%)", f"{distance_metrics['TD_Rel']:.1f}")
    
    st.plotly_chart(
        plot_distance_timeline(df, player_name, selected_date, selected_microcycle),
        use_container_width=True
    )

def render_performance_tab(df, player_name, session_data, selected_date, selected_microcycle):
    """Render performance metrics tab content."""
    perf_metrics = get_performance_summary(session_data)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Sprints", perf_metrics['Sprints'])
    with col2:
        st.metric("High Speed Running (+19 km/h)", perf_metrics['HSR'])
    with col3:
        st.metric("+25 km/h", perf_metrics['+25 Km/h'])
    
    st.plotly_chart(
        plot_performance_timeline(df, player_name, selected_date, selected_microcycle),
        use_container_width=True
    )

def render_other_tab(df, player_name, session_data):
    """Render other metrics tab content."""
    perf_metrics = get_performance_summary(session_data)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Minutes", perf_metrics['Mins'])
    with col2:
        st.metric("Player Classification", classify_player(df, player_name))
    with col3:
        st.metric("Injury Prevention Index", perf_metrics['injury_prevention_index'])

def get_player_session_options(df, player_name):
    """Get session options for a specific player sorted by date in descending order."""
    player_sessions = df[df['PlayerID'] == player_name][['DATE', 'Microcycle']].drop_duplicates()
    player_sessions = player_sessions.sort_values('DATE', ascending=False)
    player_sessions['date_label'] = player_sessions.apply(
        lambda x: f"{x['DATE'].strftime('%Y %B %d')} - {x['Microcycle']}", axis=1
    )
    return player_sessions

def get_sorted_session_options(df):
    """Get all session options sorted by date in descending order."""
    session_options = df[['DATE', 'Microcycle']].drop_duplicates()
    session_options = session_options.sort_values('DATE', ascending=False)
    session_options['date_label'] = session_options.apply(
        lambda x: f"{x['DATE'].strftime('%Y %B %d')} - {x['Microcycle']}", axis=1
    )
    return session_options

def main():
    if not check_password():
        st.stop()
    
    try:
        # Load data
        df = load_and_prepare_data("data/data.csv")
        
        # Show menu
        choice = show_menu()
        
        if choice == "Player Analysis":
            st.title("Player Physical Profile Analysis")
            
            # Player selection
            player_name = st.selectbox("Select Player", sorted(df['PlayerID'].unique()))
            
            # Get sessions for selected player
            player_sessions = get_player_session_options(df, player_name)
            
            if not player_sessions.empty:
                # Session selection with sorted dates
                selected_session = st.selectbox(
                    "Select Session",
                    player_sessions['date_label']
                )
                
                selected_date = player_sessions[
                    player_sessions['date_label'] == selected_session
                ]['DATE'].iloc[0].date()
                selected_microcycle = player_sessions[
                    player_sessions['date_label'] == selected_session
                ]['Microcycle'].iloc[0]
                
                # Get session data
                session_data = df[
                    (df['DATE'].dt.date == selected_date) & 
                    (df['Microcycle'] == selected_microcycle) &
                    (df['PlayerID'] == player_name)
                ]
                
                if not session_data.empty:
                    # Create tabs with custom CSS class
                    st.markdown('<div class="stTab">', unsafe_allow_html=True)
                    speed_tab, accel_tab, distance_tab, perf_tab, other_tab = st.tabs([
                        "Speed Metrics",
                        "Acceleration & Deceleration",
                        "Distance Metrics",
                        "Performance Metrics",
                        "Other"
                    ])
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Render content for each tab
                    with speed_tab:
                        render_speed_tab(df, player_name, session_data, selected_date, selected_microcycle)
                    
                    with accel_tab:
                        render_acceleration_tab(df, player_name, session_data, selected_date, selected_microcycle)
                    
                    with distance_tab:
                        render_distance_tab(df, player_name, session_data, selected_date, selected_microcycle)
                    
                    with perf_tab:
                        render_performance_tab(df, player_name, session_data, selected_date, selected_microcycle)
                    
                    with other_tab:
                        render_other_tab(df, player_name, session_data)
                else:
                    st.warning("No data available for the selected player and session.")
            else:
                st.warning("No sessions available for the selected player.")
                
        else:  # Team Analysis
            st.title("Team GPS Analysis")
            
            # Session selection with sorted dates
            session_options = get_sorted_session_options(df)
            selected_session = st.selectbox(
                "Select Session",
                session_options['date_label']
            )
            
            selected_date = session_options[
                session_options['date_label'] == selected_session
            ]['DATE'].iloc[0].date()
            selected_microcycle = session_options[
                session_options['date_label'] == selected_session
            ]['Microcycle'].iloc[0]
            
            # Calculate team metrics
            # Calculate team metrics
            team_metrics = calculate_team_metrics(df, selected_date, selected_microcycle)
            
            if not team_metrics.empty:
                # Display team metrics
                st.header("Team Overview")
                col1, col2, col3, col4, col5, col6 = st.columns(6)
                with col1:
                    st.metric("Average Distance (m)", f"{team_metrics['TD'].mean():.0f}")
                with col2:
                    st.metric("Average Max Speed (km/h)", f"{team_metrics['Max Speed'].mean():.1f}")
                with col3:
                    st.metric("Total Team Sprints", f"{team_metrics['Sprints'].sum():.0f}")
                with col4:
                    st.metric("Average HSR (+19 km/h)", f"{team_metrics['HSR'].mean():.1f}")
                with col5:
                    st.metric("Average +25 km/h", f"{team_metrics['+25 Km/h'].mean():.1f}")
                with col6:
                    st.metric("Total Team Minutes", f"{team_metrics['Mins'].sum():.0f}")
                
                # Team visualizations
                st.header("Team Performance Visualizations")
                fig_team_distance, fig_team_sprints = plot_team_metrics(
                    calculate_team_metrics(df),
                    selected_date
                )
                st.plotly_chart(fig_team_distance, use_container_width=True)
                st.plotly_chart(fig_team_sprints, use_container_width=True)
            else:
                st.warning("No team data available for the selected session.")
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.error("Please check if the data file exists and has the correct format.")

if __name__ == "__main__":
    main()