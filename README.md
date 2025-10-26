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

```

---

## File 2: `vbb_analysis_and_app.ipynb`

(Create this Jupyter Notebook. This helps explore the logic before building the app.)

**(Markdown Cell)**
```markdown
# VBB Public Transport Analysis & Streamlit App Logic

This notebook outlines the steps to fetch data from the VBB API, process it, and prepare the logic for a Streamlit dashboard.

**IMPORTANT:**
* You **MUST** obtain your own API key from the VBB developer portal.
* The exact API endpoints and JSON response structures shown here are **examples** and might differ from the actual VBB API. You'll need to consult the official VBB API documentation.
* Error handling should be more robust in a production app.
```

**(Markdown Cell)**
```markdown
## 1. Setup and Configuration
Import libraries and set up API key access (using a config file here for example).
```

**(Code Cell)**
```python
import requests
import pandas as pd
import json
from datetime import datetime, timedelta
import os
import warnings

warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', 50)

# --- Configuration ---
# OPTION 1: Use a config.py file (Make sure config.py is in .gitignore!)
try:
    import config
    API_KEY = config.VBB_API_KEY
    print("API Key loaded from config.py")
except (ImportError, AttributeError):
    # OPTION 2: Use an Environment Variable (Recommended for deployment)
    API_KEY = os.getenv('VBB_API_KEY')
    if API_KEY:
        print("API Key loaded from environment variable VBB_API_KEY")
    else:
        # OPTION 3: Placeholder (Replace this with your actual key if testing directly)
        API_KEY = "YOUR_VBB_API_KEY_HERE" # <<<--- REPLACE THIS OR USE Option 1 or 2
        print("API Key using placeholder - replace it!")

# --- VBB API Example Endpoints (These are illustrative - CHECK VBB DOCS!) ---
BASE_URL = "https://vbb-api-endpoint.example.com/v1" # Replace with actual base URL
LOCATION_SEARCH_ENDPOINT = f"{BASE_URL}/locations"
DEPARTURES_ENDPOINT = f"{BASE_URL}/stops/{{stop_id}}/departures" # Uses f-string formatting later

# Headers often needed for APIs
HEADERS = {'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'}

print("Setup complete.")
```

**(Markdown Cell)**
```markdown
## 2. API Interaction Functions

Functions to search for stations and get departures.
```

**(Code Cell)**
```python
def search_station(query):
    """Searches for a station ID based on a query string."""
    if not API_KEY or API_KEY == "YOUR_VBB_API_KEY_HERE":
        print("API Key not configured.")
        # Return dummy data for structure example
        return [{'id': '900000100001', 'name': 'Example Station A (Dummy)'},
                {'id': '900000100002', 'name': 'Example Station B (Dummy)'}]

    params = {'query': query, 'results': 5} # Limit results
    try:
        response = requests.get(LOCATION_SEARCH_ENDPOINT, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        # Assuming the API returns a list of location objects directly or under a key like 'locations'
        data = response.json()
        # --- Adjust based on actual API response structure ---
        if isinstance(data, list):
             # Filter only stations (example: check if 'type' is 'stop')
            stations = [loc for loc in data if loc.get('type') == 'stop']
            return stations[:5] # Return top 5
        elif 'locations' in data and isinstance(data['locations'], list):
            stations = [loc for loc in data['locations'] if loc.get('type') == 'stop']
            return stations[:5]
        else:
            print("Unexpected API response format for locations.")
            return []
        # --- End Adjustment section ---

    except requests.exceptions.RequestException as e:
        print(f"Error searching for station: {e}")
        return [] # Return empty list on error

def get_departures(stop_id, duration_minutes=60):
    """Gets departures for a specific stop ID for the next X minutes."""
    if not API_KEY or API_KEY == "YOUR_VBB_API_KEY_HERE":
        print("API Key not configured.")
        # Return dummy data for structure example
        return [{'line': {'name': 'S1'}, 'direction': 'Destination A', 'when': '2025-10-26T10:15:00+01:00', 'plannedWhen': '2025-10-26T10:15:00+01:00', 'delay': 0},
                {'line': {'name': 'U2'}, 'direction': 'Destination B', 'when': '2025-10-26T10:18:00+01:00', 'plannedWhen': '2025-10-26T10:17:00+01:00', 'delay': 60}]

    endpoint = DEPARTURES_ENDPOINT.format(stop_id=stop_id)
    params = {'duration': duration_minutes}
    try:
        response = requests.get(endpoint, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        # Assuming the API returns a list of departure objects directly or under a key like 'departures'
        data = response.json()
        # --- Adjust based on actual API response structure ---
        if isinstance(data, list):
            return data
        elif 'departures' in data and isinstance(data['departures'], list):
            return data['departures']
        else:
            print("Unexpected API response format for departures.")
            return []
        # --- End Adjustment section ---

    except requests.exceptions.RequestException as e:
        print(f"Error getting departures: {e}")
        return []

# --- Example Usage ---
print("Example Station Search for 'Potsdam Hbf':")
example_stations = search_station("Potsdam Hbf")
print(example_stations)

if example_stations:
    example_stop_id = example_stations[0]['id'] # Use the first result's ID
    print(f"\nExample Departures for ID {example_stop_id}:")
    example_departures = get_departures(example_stop_id, 30) # Get next 30 mins
    # Print first few departures for inspection
    print(json.dumps(example_departures[:2], indent=2))
else:
    print("\nCould not get example station ID.")

```

**(Markdown Cell)**
```markdown
## 3. Data Processing Function

Turn the raw JSON departure list into a structured Pandas DataFrame.
```

**(Code Cell)**
```python
def process_departures(departures_json):
    """Processes the JSON list of departures into a Pandas DataFrame."""
    processed_data = []
    if not departures_json:
        return pd.DataFrame(columns=['Line', 'Direction', 'Scheduled', 'Expected', 'Delay (Min)'])

    for dep in departures_json:
        try:
            # --- Adjust dictionary keys based on actual API response ---
            line_name = dep.get('line', {}).get('name', 'N/A')
            direction = dep.get('direction', 'N/A')
            scheduled_time_str = dep.get('plannedWhen')
            expected_time_str = dep.get('when') # 'when' usually includes delay

            # VBB API often returns delay in seconds directly
            delay_seconds = dep.get('delay')

            scheduled_dt = pd.to_datetime(scheduled_time_str) if scheduled_time_str else None
            expected_dt = pd.to_datetime(expected_time_str) if expected_time_str else scheduled_dt # Use scheduled if expected is missing

            delay_minutes = None
            if delay_seconds is not None:
                delay_minutes = delay_seconds // 60 # Convert seconds to minutes
            elif scheduled_dt and expected_dt:
                 # Calculate delay if not provided directly
                 time_diff = expected_dt - scheduled_dt
                 delay_minutes = round(time_diff.total_seconds() / 60)
            # --- End Adjustment section ---

            processed_data.append({
                'Line': line_name,
                'Direction': direction,
                'Scheduled': scheduled_dt.strftime('%H:%M') if scheduled_dt else 'N/A',
                'Expected': expected_dt.strftime('%H:%M') if expected_dt else 'N/A',
                'Delay (Min)': int(delay_minutes) if delay_minutes is not None else 0 # Default delay to 0 if unknown
            })
        except Exception as e:
            print(f"Error processing departure record: {dep} - Error: {e}") # Log errors for debugging
            continue # Skip problematic records

    df_departures = pd.DataFrame(processed_data)
    # Sort by expected time
    # df_departures.sort_values(by='Expected', inplace=True) # Sorting might be complex if times are just H:M strings
    return df_departures

# --- Example Usage ---
if 'example_departures' in locals():
    print("\nProcessing example departures into DataFrame:")
    df_processed = process_departures(example_departures)
    display(df_processed.head())
else:
    print("\nNo example departures fetched, skipping processing.")

```

**(Markdown Cell)**
```markdown
## 4. Streamlit App Logic (Conceptual)

This section outlines how the functions above would be used in a `streamlit run app.py` script.

**`app.py` would contain:**
```python
# import streamlit as st
# import pandas as pd
# # Import the functions defined above (search_station, get_departures, process_departures)
# # Or include their definitions directly in app.py

# st.title("VBB Public Transport Departures 🚆")

# # --- Station Search ---
# station_query = st.text_input("Search for a station:", "Potsdam Hbf")
# search_results = []
# if station_query:
#     search_results = search_station(station_query)

# if search_results:
#     # Create a dictionary for easy mapping from name to ID
#     station_options = {station['name']: station['id'] for station in search_results}
#     selected_station_name = st.selectbox("Select a station:", options=station_options.keys())
#     selected_station_id = station_options[selected_station_name]

#     st.write(f"Showing departures for: **{selected_station_name}** (ID: {selected_station_id})")

#     # --- Fetch and Display Departures ---
#     if st.button("Refresh Departures"):
#         departures_json = get_departures(selected_station_id, duration_minutes=60)
#         df_departures = process_departures(departures_json)
#         st.session_state['departures_df'] = df_departures # Store in session state to persist data
#     else:
#         # Load from session state if available, otherwise fetch initial data
#         if 'departures_df' not in st.session_state:
#              departures_json = get_departures(selected_station_id, duration_minutes=60)
#              df_departures = process_departures(departures_json)
#              st.session_state['departures_df'] = df_departures
#         else:
#              df_departures = st.session_state['departures_df']


#     if not df_departures.empty:
#         st.dataframe(df_departures)

#         # --- Basic Visualization Example ---
#         st.subheader("Average Delay per Line (Current View)")
#         # Ensure 'Delay (Min)' is numeric - it should be from process_departures
#         avg_delay = df_departures.groupby('Line')['Delay (Min)'].mean().sort_values(ascending=False)
#         # Filter out lines with 0 average delay if desired
#         avg_delay = avg_delay[avg_delay > 0]

#         if not avg_delay.empty:
#             st.bar_chart(avg_delay)
#         else:
#             st.write("No delays recorded in the current view.")

#     else:
#         st.warning("No departure data available for the selected station.")

# else:
#     if station_query: # Only show 'not found' if a search was attempted
#          st.error("Station not found or API error.")

```

**(Markdown Cell)**
```markdown
## 5. Next Steps

1.  **Refine API Calls:** Get actual VBB API key, find correct endpoints, and adjust `search_station`, `get_departures`, and `process_departures` to match the real API structure (JSON keys, data types, error formats).
2.  **Create `app.py`:** Copy the logic from section 4 into a `app.py` file. Import the necessary functions or define them within the script.
3.  **Secure API Key:** Implement proper API key handling (environment variables are best).
4.  **Enhance Dashboard:** Add more visualizations (on-time percentage, delay distributions), error handling, potentially caching API results briefly to avoid hitting rate limits.
5.  **Test Thoroughly:** Test with various stations and edge cases.
6.  **(Optional) Deploy:** Use Streamlit Community Cloud or another platform.
```

---

## File 3: `app.py`

(Create this file. Copy the *conceptual* Streamlit code from Section 4 of the notebook above, uncomment it, and refine it based on the actual VBB API details you find.)

```python
# --- app.py ---
import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime, timedelta
import os

# --- Configuration & API Setup ---
# (Copy relevant API_KEY loading and Endpoint definitions from Notebook Cell 2)
# IMPORTANT: Use environment variables for API key in deployed apps!
API_KEY = os.getenv('VBB_API_KEY', "YOUR_VBB_API_KEY_HERE") # Fallback to placeholder
BASE_URL = "[https://vbb-api-endpoint.example.com/v1](https://vbb-api-endpoint.example.com/v1)" # Replace with actual base URL
LOCATION_SEARCH_ENDPOINT = f"{BASE_URL}/locations"
DEPARTURES_ENDPOINT = f"{BASE_URL}/stops/{{stop_id}}/departures"
HEADERS = {'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'}

# --- API Interaction Functions ---
# (Copy the definitions of search_station and get_departures from Notebook Cell 3)
# Make sure they are adapted for the REAL VBB API structure and use BASE_URL etc.
def search_station(query):
    """Searches for a station ID based on a query string. (ADAPT TO REAL API)"""
    if not API_KEY or API_KEY == "YOUR_VBB_API_KEY_HERE":
        st.error("API Key not configured.")
        return [{'id': '900000100001', 'name': 'Example Station A (Dummy)'},
                {'id': '900000100002', 'name': 'Example Station B (Dummy)'}]
    params = {'query': query, 'results': 5}
    try:
        response = requests.get(LOCATION_SEARCH_ENDPOINT, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        # --- Adjust based on actual API response structure ---
        stations = []
        if isinstance(data, list):
             stations = [loc for loc in data if loc.get('type') == 'stop'] # Example filter
        elif 'locations' in data and isinstance(data['locations'], list):
             stations = [loc for loc in data['locations'] if loc.get('type') == 'stop']
        else:
             st.warning("Unexpected API response format for locations.")
        return stations[:5] # Return top 5
        # --- End Adjustment section ---
    except requests.exceptions.RequestException as e:
        st.error(f"Error searching for station: {e}")
        return []

def get_departures(stop_id, duration_minutes=60):
    """Gets departures for a specific stop ID. (ADAPT TO REAL API)"""
    if not API_KEY or API_KEY == "YOUR_VBB_API_KEY_HERE":
        st.error("API Key not configured.")
        return [{'line': {'name': 'S1'}, 'direction': 'Destination A', 'when': '2025-10-26T10:15:00+01:00', 'plannedWhen': '2025-10-26T10:15:00+01:00', 'delay': 0},
                {'line': {'name': 'U2'}, 'direction': 'Destination B', 'when': '2025-10-26T10:18:00+01:00', 'plannedWhen': '2025-10-26T10:17:00+01:00', 'delay': 60}]
    endpoint = DEPARTURES_ENDPOINT.format(stop_id=stop_id)
    params = {'duration': duration_minutes, 'results': 20} # Limit results
    try:
        response = requests.get(endpoint, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        # --- Adjust based on actual API response structure ---
        if isinstance(data, list):
             return data
        elif 'departures' in data and isinstance(data['departures'], list):
             return data['departures']
        else:
             st.warning("Unexpected API response format for departures.")
             return []
        # --- End Adjustment section ---
    except requests.exceptions.RequestException as e:
        st.error(f"Error getting departures: {e}")
        return []

# --- Data Processing Function ---
# (Copy the definition of process_departures from Notebook Cell 4)
# Make sure it uses the correct keys from the REAL API response
def process_departures(departures_json):
    """Processes the JSON list of departures into a Pandas DataFrame. (ADAPT TO REAL API)"""
    processed_data = []
    if not departures_json:
        return pd.DataFrame(columns=['Line', 'Direction', 'Scheduled', 'Expected', 'Delay (Min)'])
    for dep in departures_json:
        try:
            line_name = dep.get('line', {}).get('name', 'N/A')
            direction = dep.get('direction', 'N/A')
            scheduled_time_str = dep.get('plannedWhen')
            expected_time_str = dep.get('when')
            delay_seconds = dep.get('delay') # VBB often provides delay in seconds

            scheduled_dt = pd.to_datetime(scheduled_time_str) if scheduled_time_str else None
            expected_dt = pd.to_datetime(expected_time_str) if expected_time_str else scheduled_dt

            delay_minutes = None
            if delay_seconds is not None:
                # Floor division to get whole minutes
                delay_minutes = delay_seconds // 60
            elif scheduled_dt and expected_dt:
                 time_diff = expected_dt - scheduled_dt
                 delay_minutes = round(time_diff.total_seconds() / 60)

            processed_data.append({
                'Line': line_name,
                'Direction': direction,
                'Scheduled': scheduled_dt.strftime('%H:%M') if scheduled_dt else 'N/A',
                'Expected': expected_dt.strftime('%H:%M') if expected_dt else 'N/A',
                'Delay (Min)': int(delay_minutes) if delay_minutes is not None else 0
            })
        except Exception as e:
            # In a streamlit app, maybe log differently or show a warning
            print(f"Error processing departure record: {dep} - Error: {e}")
            continue
    df_departures = pd.DataFrame(processed_data)
    # Convert Delay to numeric, coercing errors
    df_departures['Delay (Min)'] = pd.to_numeric(df_departures['Delay (Min)'], errors='coerce').fillna(0).astype(int)
    return df_departures

# --- Streamlit App Layout ---
st.set_page_config(layout="wide") # Use wide layout
st.title("VBB Public Transport Departures 🚆")
st.markdown("Monitor near real-time departures and delays for Berlin/Potsdam stations.")

# --- Station Search ---
col1, col2 = st.columns([3, 1]) # Make search input wider

with col1:
    station_query = st.text_input("Search for a VBB station:", "Potsdam Hbf", label_visibility="collapsed", placeholder="Enter station name (e.g., Potsdam Hbf)")

# Use session state to store search results and selected station ID
if 'search_results' not in st.session_state:
    st.session_state['search_results'] = []
if 'selected_station_id' not in st.session_state:
    st.session_state['selected_station_id'] = None
if 'selected_station_name' not in st.session_state:
    st.session_state['selected_station_name'] = None

# Perform search only if query changes or initially
if station_query != st.session_state.get('last_query', ''):
    with st.spinner("Searching for stations..."):
        st.session_state['search_results'] = search_station(station_query)
        st.session_state['last_query'] = station_query
        # Reset selection if search changes
        st.session_state['selected_station_id'] = None
        st.session_state['selected_station_name'] = None


# --- Station Selection ---
if st.session_state['search_results']:
    station_options = {station['name']: station['id'] for station in st.session_state['search_results']}
    # Use index to handle potential selection persistence issues
    station_names = list(station_options.keys())
    # Pre-select based on session state if available
    current_selection_index = 0
    if st.session_state['selected_station_name'] in station_names:
        current_selection_index = station_names.index(st.session_state['selected_station_name'])

    selected_station_name = st.selectbox(
        "Select station from results:",
        options=station_names,
        index=current_selection_index,
        key='station_select' # Use a key to help Streamlit manage state
        )

    # Update session state based on selection
    if selected_station_name != st.session_state['selected_station_name']:
         st.session_state['selected_station_name'] = selected_station_name
         st.session_state['selected_station_id'] = station_options[selected_station_name]
         # Clear old departures when station changes
         if 'departures_df' in st.session_state:
             del st.session_state['departures_df']
         st.rerun() # Rerun to fetch data for the new station immediately

    # Store the ID just in case name isn't unique, though unlikely for top results
    st.session_state['selected_station_id'] = station_options.get(st.session_state['selected_station_name'])

else:
    if station_query: # Only show 'not found' if a search was attempted
         st.warning("No stations found matching your query.")
    st.session_state['selected_station_id'] = None # Clear station ID if no results


# --- Fetch and Display Departures ---
if st.session_state['selected_station_id']:
    st.subheader(f"Departures for: {st.session_state['selected_station_name']}")

    # Button to manually refresh
    if st.button("🔄 Refresh"):
        with st.spinner(f"Fetching departures for {st.session_state['selected_station_name']}..."):
            departures_json = get_departures(st.session_state['selected_station_id'], duration_minutes=60)
            df_departures = process_departures(departures_json)
            st.session_state['departures_df'] = df_departures # Update session state
            st.rerun() # Rerun to display updated data immediately

    # Fetch initial data or load from state
    if 'departures_df' not in st.session_state:
        with st.spinner(f"Fetching initial departures for {st.session_state['selected_station_name']}..."):
            departures_json = get_departures(st.session_state['selected_station_id'], duration_minutes=60)
            st.session_state['departures_df'] = process_departures(departures_json)

    # Display the DataFrame
    df_display = st.session_state.get('departures_df', pd.DataFrame())

    if not df_display.empty:
        # Displaying the table
        st.dataframe(df_display, use_container_width=True)

        # --- Basic Visualization Example ---
        st.subheader("Average Delay per Line (Current View)")
        if 'Delay (Min)' in df_display.columns:
            # Ensure delays are positive for this chart
            positive_delays = df_display[df_display['Delay (Min)'] > 0]
            if not positive_delays.empty:
                 avg_delay = positive_delays.groupby('Line')['Delay (Min)'].mean().sort_values(ascending=False).head(15) # Show top 15 delayed lines
                 st.bar_chart(avg_delay)
            else:
                 st.info("No positive delays recorded in the current view.")
        else:
            st.warning("Delay information not available for visualization.")

    else:
        st.warning(f"No departure data currently available for {st.session_state['selected_station_name']}.")

elif not station_query:
     st.info("Enter a station name above to search.")

st.markdown("---")
st.caption("Data fetched from VBB API (structure based on examples). Requires API key.")

```

---

## File 4: `requirements.txt`

(Create this file)

```
requests
pandas
streamlit
# Optional: Add numpy if not implicitly installed by pandas
```

---

## File 5: `.gitignore`

(Create this file)

```gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Jupyter Notebook Checkpoints
.ipynb_checkpoints

# Environment directories
venv/
env/
.env/
.venv/

# Secrets / Config files
config.py
*.env

# Streamlit secrets
.streamlit/secrets.toml

# macOS / Windows system files
.DS_Store
Thumbs.db
```
*(Self-correction: Added `config.py` and Streamlit secrets to gitignore)*.

---

## File 6: `config.py` (Optional, but Recommended)

(Create this file ONLY IF you choose Option 1 for the API key. **MAKE SURE IT'S IN .gitignore!**)

```python
# config.py
VBB_API_KEY = "YOUR_ACTUAL_VBB_API_KEY_GOES_HERE"
```

---

This provides the complete setup. The most crucial next step for you is to research the actual VBB API documentation, get a key, and update the API interaction functions (`search_station`, `get_departures`) and the processing function (`process_departures`) in both the notebook and `app.py` to match the real API structure. Good luck! 🚀
