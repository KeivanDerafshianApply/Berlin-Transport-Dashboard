# VBB Public Transport Performance Dashboard 🚆💨

This project aims to monitor and analyze the performance (delays, departures) of public transport in the Berlin/Potsdam area using data fetched from the VBB (Verkehrsverbund Berlin-Brandenburg) API. The analysis and visualization are presented through an interactive web application built with **Streamlit**.

## Project Goal

* Fetch near real-time departure/arrival data for selected public transport stations via the VBB API.
* Process the API response (JSON) to extract relevant information like line number, destination, scheduled time, actual/estimated time, and delay.
* Calculate key performance indicators (e.g., average delay per line, on-time percentage).
* Display the current departures and delay information in an interactive Streamlit dashboard.
* Allow users to select a station and refresh the data.

## Data Source

* **VBB API:** The primary data source is the public API provided by VBB. Access typically requires registration for an API key via their developer portal (research needed to find the specific portal and endpoints). Common endpoints might include searching for stations by name and getting departure boards for a specific station ID.
    * *(Placeholder/Example endpoints might be used in the code)*

## Methodology

1.  **API Interaction (Python - `requests`):**
    * Functions were created to interact with the VBB API endpoints.
    * Requires a valid API key (stored securely, e.g., in environment variables or a `config.py` file).
    * Handles API requests to search for station IDs and fetch departure data.

2.  **Data Processing (Python - `pandas`, `json`):**
    * Parsed the JSON responses from the API.
    * Extracted key fields (line, direction, scheduled time, estimated time, delay).
    * Converted timestamps to readable formats and calculated delays in minutes.
    * Structured the relevant data into Pandas DataFrames for analysis and display.

3.  **Dashboard Development (Python - `streamlit`):**
    * Created a Streamlit application (`app.py`).
    * Implemented UI elements: Title, text input for station search, selectbox/dropdown for choosing a specific station from search results, refresh button.
    * Displayed the processed departure data in a clean table format.
    * Added basic visualizations (e.g., bar chart showing average delay per line for the current view).

4.  **Deployment (Optional):**
    * The Streamlit app can be deployed using services like Streamlit Community Cloud for public access.

## Key Features of the Dashboard

* **Station Search:** Find stations within the VBB network.
* **Real-time Departures:** View upcoming departures for the selected station.
* **Delay Information:** See calculated delays for each departure.
* **Basic Analysis:** View simple charts summarizing performance (e.g., average delays).
* **Auto/Manual Refresh:** (Can be implemented in Streamlit)

## How to Run

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd vbb-dashboard
    ```
2.  **Set up VBB API Key:**
    * Register for an API key from the official VBB developer portal.
    * **Crucially:** Store your API key securely. You can:
        * Create a `config.py` file (add it to `.gitignore`!) with `API_KEY = "YOUR_KEY"`.
        * Or set it as an environment variable (`export VBB_API_KEY="YOUR_KEY"` on Mac/Linux, `set VBB_API_KEY="YOUR_KEY"` on Windows). The code will need to be adapted to read from the chosen method.
3.  **Set up Python environment:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the Streamlit App:**
    ```bash
    streamlit run app.py
    ```
    This will start a local web server, and your browser should open to the interactive dashboard.

## Tools Used

* **Python:** `requests`, `pandas`, `streamlit`, `json`, `datetime`
* **VBB API**
* **Streamlit** (for dashboarding)
* **Jupyter Notebook** (for initial exploration)
