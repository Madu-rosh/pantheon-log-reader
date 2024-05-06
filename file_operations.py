# file_operations.py
import os
import streamlit as st
import base64
from pathlib import Path
import re  # Import the regular expression library
from config import archive_extensions

def list_directory(path):
    """List directories and files recursively."""
    items = []
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            items.append({"name": entry.name, "type": "directory", "path": entry.path})
        elif entry.is_file(follow_symlinks=False):
            items.append({"name": entry.name, "type": "file", "path": entry.path})
    return items

def render_file_tree(items, base_path, filter_query=""):
    """Recursive function to display directories and files as an expandable tree in the sidebar with filtering."""
    for item in sorted(items, key=lambda x: (x['type'], x['name'])):
        if filter_query.lower() in item['name'].lower():
            if item['type'] == 'directory':
                with st.sidebar.expander(item['name']):
                    sub_items = list_directory(item['path'])
                    render_file_tree(sub_items, base_path, filter_query)
            elif item['type'] == 'file':
                if st.sidebar.button(item['name'], key=item['path']):
                    st.session_state.selected_file_path = item['path']

def display_file_content():
    """Display the contents of a file in the main area, clearing previous errors before processing."""
    if 'selected_file_path' in st.session_state:
        # Clear previous error messages
        if 'error' in st.session_state:
            del st.session_state['error']

        file_path = Path(st.session_state.selected_file_path)  # Use Pathlib for robust path handling
        file_extension = file_path.suffix.lower()

        try:
            if file_extension in archive_extensions:
                handle_compressed_file(file_path)
            else:
                with open(file_path, "r", encoding='utf-8') as file:
                    content = file.read()
                    # Use 'log' language syntax highlighting for log files, or auto-detect based on extension
                    language = 'log' if file_extension == '.log' else None
                    st.code(content, language=language, line_numbers=True)
        except Exception as e:
            error_message = f"Error reading {file_path}: {str(e)}"
            st.error(error_message)
            st.session_state.error = error_message  # Store errors in session state for display

def handle_compressed_file(file_path):
    """Provide a download link for compressed files."""
    try:
        file_extension = file_path.suffix.lower()
        mime_type = archive_extensions.get(file_extension, 'application/octet-stream')  # Default to octet-stream if not found
        with open(file_path, "rb") as f:
            bytes = f.read()
            b64 = base64.b64encode(bytes).decode()
            href = f'<a href="data:{mime_type};base64,{b64}" download="{os.path.basename(file_path)}">Download {os.path.basename(file_path)}</a>'
            st.markdown(href, unsafe_allow_html=True)
            st.info("This is a compressed file (e.g., old log archives). Please download and check locally.")
    except Exception as e:
        st.error(f"Error processing {file_path}: {e}")

def search_files(base_path):
    """Search bar for files with a clear button styled as an 'X' inside the text input."""
    col1, col2 = st.sidebar.columns([0.9, 0.1])
    with col1:
        search_query = st.text_input("Search files", value=st.session_state.get("file_search", ""), key="file_search")
    with col2:
        if st.button("X", key="clear_search"):
            if "file_search" in st.session_state:
                del st.session_state['file_search']  # Removing instead of setting to empty to fully clear the field
            st.rerun()  # Rerun the app to refresh the state without the search query

    items = list_directory(base_path)
    if "file_search" in st.session_state:
        render_file_tree(items, base_path, st.session_state["file_search"])
    else:
        render_file_tree(items, base_path)