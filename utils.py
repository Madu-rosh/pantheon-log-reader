def get_wsl_path(windows_path):
    """Converts a Windows path to its equivalent WSL path. Supports paths from any drive."""
    if isinstance(windows_path, bytes):
        windows_path = windows_path.decode('utf-8')
    
    # Check if the path starts with a drive letter followed by a colon and a backslash (e.g., 'C:\')
    if len(windows_path) > 2 and windows_path[1] == ':' and windows_path[2] == '\\':
        drive_letter = windows_path[0].lower()  # Convert drive letter to lowercase
        # Replace backslashes with forward slashes and replace the drive letter with '/mnt/{drive_letter}'
        return f"/mnt/{drive_letter}" + windows_path[2:].replace('\\', '/')
    else:
        # If the path does not start with a drive letter, assume it's already a WSL or relative path
        return windows_path

# Example Usage
if __name__ == "__main__":
    print(get_wsl_path("C:\\Users\\Example\\file.txt"))  # Output: /mnt/c/Users/Example/file.txt
    print(get_wsl_path("D:\\Work\\project\\data.csv"))  # Output: /mnt/d/Work/project/data.csv
