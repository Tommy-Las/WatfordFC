import streamlit as st

def show_menu():
    """Display the navigation menu."""
    menu = ["Player Analysis", "Team Analysis"]
    choice = st.sidebar.selectbox("Navigation", menu)
    return choice