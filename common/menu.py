import streamlit as st

def show_menu():
    """Display the navigation menu with logo and navigation links."""
    # Display logo
    st.sidebar.image("assets/logo.png", width=100)
    st.sidebar.title("Navigation")
    
    # Initialize session state for page selection
    if 'page' not in st.session_state:
        st.session_state.page = "Player Analysis"
    
    # Create navigation buttons vertically
    if st.sidebar.button(
        "Player Analysis",
        key="player_btn",
        type="primary"
    ):
        st.session_state.page = "Player Analysis"
        st.experimental_rerun()
    
    if st.sidebar.button(
        "Team Analysis",
        key="team_btn",
        type="primary"
    ):
        st.session_state.page = "Team Analysis"
        st.experimental_rerun()
    
    # Add logout button
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout", key="logout_btn"):
        st.session_state.clear()
        st.experimental_rerun()
    
    return st.session_state.page