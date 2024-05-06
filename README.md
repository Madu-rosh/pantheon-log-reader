
# Pantheon Log Reader

This repository contains the source code for Pantheon Log Reader, a Streamlit-based web application designed to read log files downloaded from each site on Pantheon using a GUI.

## Features

- **Download Logs from Pantheon**: Download log files from pantheon related to each UUID
- **File Exploration**: Browse log files within a designated directory using a sidebar interface.
- **File Content Display**: View content of selected log files directly in the browser.
- **Search Functionality**: Quickly find log files by name through a dynamic search bar.

## Prerequisites

Before you can run this application, you'll need to have the following installed:
- Python 3.6 or higher
- pip (Python package installer)

## Installation

Follow these steps to get your development environment set up:

1. **Clone the repository**
   ```bash
   git clone https://github.com/Madu-rosh/pantheon-log-reader
   cd pantheon-log-reader
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

- **`config.py`**: Set the necessary configuration variables such as `download_location`.
- Ensure all paths and external dependencies are correctly configured in your environment files.

## Running the Application

To run the application, execute the following command in your terminal:

```bash
streamlit run main.py
```

Navigate to `http://localhost:8501` in your web browser to see the application in action.

## Usage

- **Navigating the Application**: Use the sidebar to browse and search for log files. Click on a log file to view its contents in the main area.
- **Viewing File Details**: Select any log file from the sidebar to see its contents displayed or download links provided for compressed files.
- **Returning to Home**: Use the 'Back to Home' button to navigate back to the initial page.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Support the Project

Appreciate the effort and help me:

<a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=V7CYQD2WJQBCQ&source=url"><img src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif"></a><span>&nbsp;</span>
<a target="_blank" title="Buy me a coffee" href="https://www.buymeacoffee.com/creativerosh"><img src="https://cdn.buymeacoffee.com/buttons/default-blue.png" alt="Buy me a coffee" height="41" width="174"></a>

Your support is much appreciated and will help ensure the continued development and improvement of this platform.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Your Name - [@your_twitter](https://twitter.com/your_twitter) - email@example.com

Project Link: [https://github.com/Madu-rosh/pantheon-log-reader](https://github.com/Madu-rosh/pantheon-log-reader)
