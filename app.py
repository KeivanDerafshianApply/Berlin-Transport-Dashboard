#!/usr/bin/env python
# coding: utf-8

# In[1]:


# --- app.py ---
import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime, timedelta
import os

# --- Configuration & API Setup ---
# IMPORTANT: Use environment variables for API key in deployed apps!
API_KEY = os.getenv('VBB_API_KEY', "YOUR_VBB_API_KEY_HERE") # Fallback to placeholder
# --- !!! REPLACE with ACTUAL VBB API details !!! ---
BASE_URL = "https://vbb-api-endpoint.example.com/v1" # Replace with actual base URL
LOCATION_SEARCH_ENDPOINT = f"{BASE_URL}/locations"
DEPARTURES_ENDPOINT = f"{BASE_URL}/stops/{{stop_id}}/departures"
# --- !!! END REPLACE section !!! ---
HEADERS = {'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'} # Adjust Auth if needed

# --- API Interaction Functions ---
# (ADAPT THESE TO THE REAL VBB API STRUCTURE AND RESPONSE KEYS)
def search_station(query):
    """Searches for a station ID based on a query string. (ADAPT TO REAL API)"""
    if not API_KEY or API_KEY == "YOUR_VBB_API_KEY_HERE":
        st.error("API Key not configured.")
        # Return dummy data for structure example ONLY if API key missing
        return [{'id': '900000100001', 'name': 'Example Station A (Dummy)'},
                {'id': '900000100002', 'name': 'Example Station B (Dummy)'}]
    params = {'query': query, 'results': 5} # Request fewer results initially
    try:
        response = requests.get(LOCATION_SEARCH_ENDPOINT, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        # --- Adjust parsing based on actual API response structure ---
        stations = []
        # Example: Check common structures
        potential_keys = ['locations', 'stopLocations', 'station'] # Common keys for lists
        found_list = None
        if isinstance(data, list):
            found_list = data
        else:
            for key in potential_keys:
                 if key in data and isinstance(data[key], list):
                     found_list = data[key]
                     break

        if found_list is not None:
             # Example filter: Check if 'type' is 'stop' or if it has an 'id'
             stations = [loc for loc in found_list if loc.get('type') == 'stop' or 'id' in loc]
        else:
             st.warning("Could not find station list in API response.")
        # --- End Adjustment section ---
        return stations[:5] # Return top 5 found stations
    except requests.exceptions.RequestException as e:
        st.error(f"Error searching for station: {e}")
        return []
    except json.JSONDecodeError:
        st.error("Error decoding API response (search).")
        return []

def get_departures(stop_id, duration_minutes=60):
    """Gets departures for a specific stop ID. (ADAPT TO REAL API)"""
    if not API_KEY or API_KEY == "YOUR_VBB_API_KEY_HERE":
        st.error("API Key not configured.")
        # Return dummy data for structure example ONLY if API key missing
        return [{'line': {'name': 'S1'}, 'direction': 'Destination A', 'when': '2025-10-26T10:15:00+01:00', 'plannedWhen': '2025-10-26T10:15:00+01:00', 'delay': 0},
                {'line': {'name': 'U2'}, 'direction': 'Destination B', 'when': '2025-10-26T10:18:00+01:00', 'plannedWhen': '2025-10-26T10:17:00+01:00', 'delay': 60}]

    endpoint = DEPARTURES_ENDPOINT.format(stop_id=stop_id)
    params = {'duration': duration_minutes, 'results': 20} # Limit number of results
    try:
        response = requests.get(endpoint, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        # --- Adjust parsing based on actual API response structure ---
        departures = []
        potential_keys = ['departures', 'journeys', 'connections'] # Common keys for lists
        found_list = None
        if isinstance(data, list):
            found_list = data
        else:
            for key in potential_keys:
                 if key in data and isinstance(data[key], list):
                     found_list = data[key]
                     break

        if found_list is not None:
            departures = found_list
        else:
             st.warning("Could not find departures list in API response.")
        # --- End Adjustment section ---
        return departures
    except requests.exceptions.RequestException as e:
        st.error(f"Error getting departures: {e}")
        return []
    except json.JSONDecodeError:
         st.error("Error decoding API response (departures).")
         return []

# --- Data Processing Function ---
# (ADAPT THESE KEY LOOKUPS TO THE REAL VBB API STRUCTURE)
def process_departures(departures_json):
    """Processes the JSON list of departures into a Pandas DataFrame. (ADAPT TO REAL API)"""
    processed_data = []
    if not departures_json:
        return pd.DataFrame(columns=['Line', 'Direction', 'Scheduled', 'Expected', 'Delay (Min)', 'Platform']) # Added Platform

    for dep in departures_json:
        try:
            # --- Adjust dictionary keys based on actual API response ---
            line_info = dep.get('line', {})
            line_name = line_info.get('name', line_info.get('productName', 'N/A')) # Try different keys
            direction = dep.get('direction', dep.get('destination', 'N/A')) # Try different keys
            scheduled_time_str = dep.get('plannedWhen', dep.get('scheduledTime'))
            expected_time_str = dep.get('when', dep.get('actualTime', scheduled_time_str)) # Fallback to scheduled if actual/when missing
            delay_seconds = dep.get('delay') # VBB often provides delay in seconds
            platform = dep.get('platform', dep.get('plannedPlatform', 'N/A')) # Try different keys

            scheduled_dt = pd.to_datetime(scheduled_time_str) if scheduled_time_str else None
            expected_dt = pd.to_datetime(expected_time_str) if expected_time_str else scheduled_dt

            delay_minutes = None
            if delay_seconds is not None:
                # Floor division to get whole minutes, handle non-numeric delay if necessary
                try:
                    delay_minutes = int(delay_seconds) // 60
                except (ValueError, TypeError):
                    delay_minutes = 0 # Default if delay is not a number
            elif scheduled_dt and expected_dt:
                 # Only calculate if times are valid datetimes
                 time_diff = expected_dt - scheduled_dt
                 delay_minutes = round(time_diff.total_seconds() / 60)

            # Ensure delay is non-negative if API sometimes gives negative for early arrivals
            if delay_minutes is not None and delay_minutes < 0:
                delay_minutes = 0

            # --- End Adjustment section ---

            processed_data.append({
                'Line': line_name,
                'Direction': direction,
                'Scheduled': scheduled_dt.strftime('%H:%M') if scheduled_dt else 'N/A',
                'Expected': expected_dt.strftime('%H:%M') if expected_dt else 'N/A',
                'Delay (Min)': int(delay_minutes) if delay_minutes is not None else 0, # Default delay to 0 if unknown
                'Platform': platform
            })
        except Exception as e:
            # In a streamlit app, maybe log differently or show a warning
            st.warning(f"Skipping record due to processing error: {e}")
            continue # Skip problematic records

    if not processed_data:
        return pd.DataFrame(columns=['Line', 'Direction', 'Scheduled', 'Expected', 'Delay (Min)', 'Platform'])

    df_departures = pd.DataFrame(processed_data)

    # Convert Delay to numeric, coercing errors AFTER DataFrame creation
    df_departures['Delay (Min)'] = pd.to_numeric(df_departures['Delay (Min)'], errors='coerce').fillna(0).astype(int)

    # Sort by Expected Time (if possible, convert to datetime first for proper sort)
    try:
        # Create a temporary datetime column for sorting if 'Expected' is just H:M
        now = datetime.now()
        df_departures['sort_time'] = df_departures['Expected'].apply(
            lambda x: datetime.strptime(f"{now.strftime('%Y-%m-%d')} {x}", '%Y-%m-%d %H:%M') if x != 'N/A' else pd.NaT
        )
        # Handle cases where expected time might wrap past midnight (needs more complex logic if times > 23:59)
        df_departures.sort_values(by='sort_time', inplace=True, na_position='last')
        df_departures.drop(columns=['sort_time'], inplace=True)
    except Exception:
        # Fallback sort if time conversion fails
        df_departures.sort_values(by=['Expected', 'Scheduled'], inplace=True)


    return df_departures

# --- Streamlit App Layout ---
st.set_page_config(layout="wide") # Use wide layout
st.title("VBB Public Transport Departures 🚆")
st.markdown("Monitor near real-time departures and delays for Berlin/Potsdam stations.")

# Check for API Key early
if not API_KEY or API_KEY == "YOUR_VBB_API_KEY_HERE":
    st.error("VBB API Key is not configured. Please set the VBB_API_KEY environment variable or update config.py.")
    st.stop() # Stop execution if no API key

# --- Station Search ---
col1, col2 = st.columns([3, 1]) # Make search input wider

with col1:
    # Use session state to keep search query persistent
    if 'station_query' not in st.session_state:
        st.session_state['station_query'] = "Potsdam Hbf" # Default value

    station_query = st.text_input(
        "Search for a VBB station:",
        value=st.session_state['station_query'],
        label_visibility="collapsed",
        placeholder="Enter station name (e.g., Potsdam Hbf)"
        )
    # Update session state if input changes
    if station_query != st.session_state['station_query']:
        st.session_state['station_query'] = station_query
        # Clear previous results and selections when query changes
        st.session_state['search_results'] = []
        st.session_state['selected_station_id'] = None
        st.session_state['selected_station_name'] = None
        if 'departures_df' in st.session_state:
            del st.session_state['departures_df'] # Clear old data


# Initialize session state keys if they don't exist
if 'search_results' not in st.session_state:
    st.session_state['search_results'] = []
if 'selected_station_id' not in st.session_state:
    st.session_state['selected_station_id'] = None
if 'selected_station_name' not in st.session_state:
    st.session_state['selected_station_name'] = None

# Trigger search automatically if query exists and results are empty (or first run)
if station_query and not st.session_state['search_results']:
    with st.spinner("Searching for stations..."):
        st.session_state['search_results'] = search_station(station_query)


# --- Station Selection ---
selected_station_name = None # Define variable outside the if block

if st.session_state['search_results']:
    # Prepare options for selectbox {name: id}
    station_options = {station.get('name', 'Unknown Name'): station.get('id', None)
                       for station in st.session_state['search_results'] if station.get('id')}

    if not station_options:
         st.warning("No valid stations found in search results.")
    else:
        station_names = list(station_options.keys())

        # Determine the default index for selectbox
        current_selection_index = 0
        if st.session_state.get('selected_station_name') in station_names:
            current_selection_index = station_names.index(st.session_state['selected_station_name'])
        elif station_names: # Default to first result if no previous selection or previous selection invalid
             st.session_state['selected_station_name'] = station_names[0]
             st.session_state['selected_station_id'] = station_options[station_names[0]]

        # Use a key to help Streamlit maintain the state of the selectbox
        selected_station_name = st.selectbox(
            "Select station from results:",
            options=station_names,
            index=current_selection_index,
            key='station_selectbox'
            )

        # Update session state ONLY if selection actually changes via UI
        if selected_station_name and selected_station_name != st.session_state.get('selected_station_name'):
             st.session_state['selected_station_name'] = selected_station_name
             st.session_state['selected_station_id'] = station_options[selected_station_name]
             # Clear old departures when station changes explicitly
             if 'departures_df' in st.session_state:
                 del st.session_state['departures_df']
             st.rerun() # Rerun immediately after user selects a new station

elif station_query: # Only show 'not found' if a search was attempted
     st.warning("No stations found matching your query or API error.")


# --- Fetch and Display Departures ---
if st.session_state.get('selected_station_id'):
    st.subheader(f"Departures for: {st.session_state.get('selected_station_name', 'N/A')}")

    # Button to manually refresh
    if st.button("🔄 Refresh Departures"):
        with st.spinner(f"Fetching departures..."):
            departures_json = get_departures(st.session_state['selected_station_id'], duration_minutes=60)
            df_departures = process_departures(departures_json)
            st.session_state['departures_df'] = df_departures # Update session state
            st.rerun() # Rerun to display updated data immediately

    # Fetch initial data if not in state, or if refresh wasn't clicked
    if 'departures_df' not in st.session_state:
        with st.spinner(f"Fetching initial departures..."):
            departures_json = get_departures(st.session_state['selected_station_id'], duration_minutes=60)
            st.session_state['departures_df'] = process_departures(departures_json)

    # Display the DataFrame from session state
    df_display = st.session_state.get('departures_df', pd.DataFrame())

    if not df_display.empty:
        # Displaying the table - use st.dataframe for better interactivity
        st.dataframe(
            df_display[['Line', 'Direction', 'Scheduled', 'Expected', 'Delay (Min)', 'Platform']],
            use_container_width=True,
            hide_index=True # Hide the default pandas index
            )

        # --- Basic Visualization Example ---
        st.subheader("Average Delay per Line (Current View)")
        if 'Delay (Min)' in df_display.columns:
            # Ensure delays are positive for this chart (or handle negative delays if meaningful)
            positive_delays = df_display[df_display['Delay (Min)'] > 0]
            if not positive_delays.empty:
                 # Group by Line and calculate mean delay
                 avg_delay = positive_delays.groupby('Line')['Delay (Min)'].mean().sort_values(ascending=False).head(15) # Show top 15 delayed lines
                 st.bar_chart(avg_delay)
            else:
                 st.info("No positive delays recorded in the current view.")
        else:
            st.warning("Delay information not available for visualization.")

    else:
        # Show message if fetch returned empty results
        st.warning(f"No departure data currently available for {st.session_state.get('selected_station_name', 'the selected station')}.")

elif not station_query:
     st.info("Enter a station name above to search.")

st.markdown("---")
st.caption("Data fetched from VBB API. Delays based on API data. Accuracy depends on API provider.")


# In[ ]:




