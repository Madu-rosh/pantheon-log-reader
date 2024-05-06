import subprocess
import os
import tempfile
import streamlit as st
from config import remote_script, download_location
from utils import get_wsl_path

def execute_script(execution_mode, site_uuid, env, keyfile, passphrase_required, key_passphrase, git_bash_path):
    if not os.path.exists(download_location):
        os.makedirs(download_location)

    script_path = get_wsl_path(remote_script) if execution_mode == "WSL" else remote_script
    base_command = f"{script_path} {site_uuid} {env}"

    st.info(base_command)

    if keyfile:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_key_file:
            tmp_key_file.write(keyfile.getvalue())
            tmp_key_file.flush()
            key_path = tmp_key_file.name

        key_path_wsl = get_wsl_path(key_path) if execution_mode == "WSL" else key_path

        agent_result = subprocess.run(["ssh-agent", "-s"], capture_output=True, text=True, shell=True)
        if agent_result.returncode != 0:
            st.error(f"Failed to start SSH agent: {agent_result.stderr.strip()}")
            return None, agent_result.stderr.strip()

        os.environ["SSH_AUTH_SOCK"] = agent_result.stdout.split(";")[0].split('=')[1].strip()
        ssh_add_command = ["ssh-add", key_path_wsl]
        if passphrase_required:
            ssh_add_command = ['echo', key_passphrase, '|', 'ssh-add', key_path_wsl]

        add_key_result = subprocess.run(ssh_add_command, capture_output=True, text=True, shell=True)
        if add_key_result.returncode != 0:
            st.error(f"Failed to add SSH key: {add_key_result.stderr.strip()}")
            return None, add_key_result.stderr.strip()

        st.success("SSH key added successfully.")

    result = subprocess.run(["wsl", "sh", "-c", base_command], capture_output=True, text=True)
    return result.stdout, result.stderr