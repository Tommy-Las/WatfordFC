import streamlit as st
import pandas as pd
from common.session import check_password
from common.menu import show_menu
from functions.player_analysis import (
    load_player_data,
    calculate_relative_metrics,
    calculate_rolling_metrics,
    classify_player,
    plot_player_metrics
)
from functions.team_analysis import calculate_team_metrics, plot_team_metrics

st.set_page_config(page_title="GPS Analysis Platform", layout="wide")

def main():
    if not check_password():
        st.stop()
    
    # Load data
    df = load_player_data("data/sample_gps_data.csv")
    
    # Show menu
    choice = show_menu()
    
    if choice == "Player Analysis":
        st.title("Player Physical Profile Analysis")
        
        # Player selection
        player_id = st.selectbox("Select Player", df['player_id'].unique())
        player_name = df[df['player_id'] == player_id]['player_name'].iloc[0]
        
        # Date range selection
        date_range = st.date_input("Select Date Range",
                                 [df['date'].min(), df['date'].max()])
        
        # Analysis type selection
        analysis_type = st.radio("Analysis Type",
                               ["Daily", "Rolling Average"])
        
        if analysis_type == "Daily":
            player_df = calculate_relative_metrics(df, player_id)
        else:
            window = st.selectbox("Select Rolling Window (Days)",
                                [3, 7, 21])
            player_df = calculate_rolling_metrics(df, player_id, window)
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Max Speed (km/h)",
                     f"{player_df[player_df['player_id'] == player_id]['max_speed'].mean():.2f}")
        with col2:
            st.metric("Total Distance (m)",
                     f"{player_df[player_df['player_id'] == player_id]['distance'].mean():.0f}")
        with col3:
            st.metric("Player Classification",
                     classify_player(df, player_id))
        
        # Display plots
        fig_speed, fig_distance = plot_player_metrics(player_df, player_id)
        st.plotly_chart(fig_speed)
        st.plotly_chart(fig_distance)
        
    else:  # Team Analysis
        st.title("Team GPS Analysis")
        
        # Calculate team metrics
        team_metrics = calculate_team_metrics(df)
        
        # Display team metrics
        st.subheader("Team Overview")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Average Team Distance (m)",
                     f"{team_metrics['distance'].mean():.0f}")
        with col2:
            st.metric("Total Team Minutes",
                     f"{team_metrics['minutes'].sum():.0f}")
        
        # Display team plots
        fig_team_distance, fig_team_sprints = plot_team_metrics(team_metrics)
        st.plotly_chart(fig_team_distance)
        st.plotly_chart(fig_team_sprints)

if __name__ == "__main__":
    main()