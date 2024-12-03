import streamlit as st

def show_menu():
    """Display the navigation menu with logo and radio-style navigation."""
    # Display logo
    st.sidebar.image("assets/logo.png", width=100)
    st.sidebar.title("Navigation")
    
    # Initialize session state for page selection
    if 'page' not in st.session_state:
        st.session_state.page = "Player Analysis"
    
    # Create radio button for navigation (acts like mutually exclusive checkboxes)
    st.session_state.page = st.sidebar.radio("", ["Player Analysis", "Team Analysis"])
    
    # Add logout button
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.experimental_rerun()
    
    return st.session_state.page