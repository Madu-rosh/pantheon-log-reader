import base64
import os
import subprocess

import streamlit as st

# UI elements
st.title("🌐 Pantheon Log Files Downloader")
site_uuid = st.text_input("Site UUID")
environments = ["dev", "test", "live"]  # List of environment options
env = st.selectbox("Environment", environments)
keyfile = st.file_uploader("Upload Private Key (optional)", accept_multiple_files=False)
passphrase_required = st.checkbox("Passphrase Required")
if passphrase_required:
    key_passphrase = st.text_input("Key Passphrase", type="password")

# Define the options and their descriptions
options = {
    "WSL": "Run the script in a local Windows machine using Windows Subsystem for Linux (WSL).",
    "Git Bash": "Run the script using Git Bash, which allows Unix command line utilities to be used on Windows.",
    "Linux Machine": "Run the script on a Linux machine or server, which can be used for development or production environments."
}

# Create two columns for the layout
col1, col2 = st.columns(2)
# In the first column, add the radio options
with col1:
    # User selects the execution environment
    execution_mode = st.radio("Select Execution Environment", list(options.keys()))

# In the second column, display the info based on the selected mode
with col2:
    if execution_mode:
        st.info(options[execution_mode])

# Conditional input for Git Bash path
if execution_mode == "Git Bash":
    git_bash_path = st.text_input("Enter Git Bash executable path (e.g., C:/Program Files/Git/bin/bash.exe)")
remote_script = "./collect-logs-sftp.sh"
download_location = "./logs"

# Define the get_wsl_path function
def get_wsl_path(windows_path):
    """Converts a Windows path to its equivalent WSL path"""
    if isinstance(windows_path, bytes):
        windows_path = windows_path.decode('utf-8')
    if windows_path.startswith("D:"):  # Assuming your script is on D: drive
        parts = windows_path.split("\\")
        return "/mnt/d/" + "/".join(parts[1:])
    else:
        # Handle other drives if needed
        return windows_path


if st.button("Run Script"):
    st.info("Running script")

    # Construct the command to execute within WSL
    wsl_command = ""
    if execution_mode == "WSL":
        if not os.path.exists(download_location):
            os.makedirs(download_location)
        
        # Add SSH key if required
        if keyfile:
            if keyfile.size > 5 * 1024 * 1024:  # Check if size is greater than 5MB
                st.error("File size exceeds 5MB limit. Please choose a smaller file.")
            else:
                st.info(f"Uploaded file size: {keyfile.size} bytes")  # Display file size
                key_path = keyfile.getvalue()  # Get the key data or temporary file path
                wsl_key_path = get_wsl_path(key_path)
                if passphrase_required:
                    encoded_passphrase = base64.b64encode(key_passphrase.encode("utf-8"))  # Encode for eval
                    wsl_command += f"eval $(ssh-agent); ssh-add {wsl_key_path}; "
                else:
                    wsl_command += f"ssh-add {wsl_key_path} "
        
        # Add script execution command
        wsl_script_path = get_wsl_path(remote_script)  # Get correct WSL path
        wsl_command += f" {wsl_script_path} {site_uuid} {env}"

    elif execution_mode == "Git Bash":
        wsl_command = f"{git_bash_path} -c \"{remote_script} {site_uuid} {env}\""

    # Execute the command within WSL
    with subprocess.Popen(
        ["wsl", "sh", "-c", wsl_command],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ) as proc:
        if passphrase_required:
            proc.communicate(encoded_passphrase)
        stdout, stderr = proc.communicate()

    # Print the output and error (if any)
    if stdout:
        st.text("Output:")
        st.text(stdout.decode())
    if stderr:
        st.text("Error:")
        st.text(stderr.decode())

    # Display results
    st.write("Files downloaded to:", download_location)
    filelist = []
    for root, dirs, files in os.walk(download_location):
        for file in files:
            filename = os.path.join(root, file)
            filelist.append(filename)
    st.write(filelist)
