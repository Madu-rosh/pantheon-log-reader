import streamlit as st
from config import options, environments, download_location
from navigation import go_to_page
from script_execution import execute_script
from file_operations import search_files, display_file_content

def home_page():
   
    st.title("🌐 Pantheon Log Files Downloader")
    site_uuid = st.text_input("Site UUID", key='site_uuid')
    env = st.selectbox("Environment", environments)
    keyfile = st.file_uploader("Upload Private Key (optional)", accept_multiple_files=False)
    if keyfile and keyfile.size > 5 * 1024 * 1024:
        st.error("File size exceeds 5MB limit. Please choose a smaller file.")
        return  # Early return to prevent further processing
    elif keyfile:
        st.info(f"Uploaded file size: {keyfile.size} bytes")

    passphrase_required = st.checkbox("Passphrase Required")
    key_passphrase = st.text_input("Key Passphrase", type="password") if passphrase_required else ""
    
    col1, col2 = st.columns(2)
    with col1:
        execution_mode = st.radio("Select Execution Environment", list(options.keys()), key='execution_mode')

    with col2:
        if execution_mode:
            st.info(options[execution_mode])

    git_bash_path = st.text_input("Enter Git Bash executable path (e.g., C:/Program Files/Git/bin/bash.exe)", key='git_bash_path')  if execution_mode == "Git Bash" else None

    if st.button("Run Script"):        
        error = execute_script(execution_mode, site_uuid, env, keyfile, passphrase_required, key_passphrase, git_bash_path)
        if error:  # Check if there's an error first
            st.error("An error occurred: " + error)
        else:
            st.success("Script executed successfully.")
            st.text(output)  # Display any output from the script execution
            go_to_page('result_page')  # Navigate to result page only if there's no error


def result_page():
    col1, col2 = st.columns([6, 2])
    with col1:
        st.title("File LookUp")
    with col2:
        if st.button("Back to Home"):
            go_to_page('home')

    st.sidebar.title("Downloaded Files")
    search_files(download_location)

    if 'output' in st.session_state:
        st.subheader("Output:")
        display_file_content()

    if 'error' in st.session_state and st.session_state.error:
        st.subheader("Error:")
        st.text(st.session_state.error)
