# config.py
options = {
    "WSL": "Run the script in a local Windows machine using Windows Subsystem for Linux (WSL).",
    "Git Bash": "Run the script using Git Bash, which allows Unix command line utilities to be used on Windows.",
    "Linux Machine": "Run the script on a Linux machine or server, which can be used for development or production environments."
}

environments = ["dev", "test", "live"]  # List of environment options

# Define a set of archive file extensions
archive_extensions = {
    '.gz': 'application/gzip',
    '.zip': 'application/zip',
    '.tar': 'application/x-tar',
    '.rar': 'application/vnd.rar',
    '.7z': 'application/x-7z-compressed',
    '.bz2': 'application/x-bzip2',
    '.xz': 'application/x-xz'
}

remote_script = "./collect-logs-sftp.sh"
download_location = "./logs" # Specify the root directory for logs
