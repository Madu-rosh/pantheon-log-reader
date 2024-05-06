# main.py
import streamlit as st
from pages import home_page, result_page

if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.page == 'home':
    home_page()
elif st.session_state.page == 'result_page':
    result_page()
