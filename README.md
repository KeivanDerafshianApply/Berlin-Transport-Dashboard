# Berlin/Potsdam Public Transport Performance Dashboard 🚆💨

This project aims to monitor and analyze the performance of public transport (like S-Bahn, U-Bahn, Tram) in the Berlin/Potsdam VBB network. It involves fetching data programmatically, processing it, and displaying key metrics and visualizations in an interactive web application built with Streamlit.

## Project Goal

My goal was to practice working with external data sources (APIs or web scraping) and build a dynamic dashboard using Python. I wanted to answer questions like:
* What are the current departure times for selected stations?
* Are there significant delays reported?
* Can we visualize punctuality trends over a short period?

## Data Source

The primary intended data source is the **VBB API** (Verkehrsverbund Berlin-Brandenburg). Accessing real-time public transport data typically requires registering for an API key and understanding the specific API endpoints for station departures, delays, etc.

* **API Interaction:** The `vbb_data_fetcher.py` script demonstrates how one might structure the code to fetch data using the `requests` library and parse the expected JSON response. *(Note: Actual API key and endpoint implementation are placeholders)*.
* **Alternative (if API is complex):** As a fallback, one could explore scraping static timetable or known disruption pages from the VBB website using libraries like `BeautifulSoup`, although this provides less dynamic information.

## Methodology

1.  **Data Acquisition (Python - `requests`):**
    * Developed a script (`vbb_data_fetcher.py`) to simulate fetching departure data from a VBB API endpoint for a specified station (e.g., Potsdam Hbf).
    * Included functions to handle potential JSON parsing and extraction of relevant fields like planned vs. actual departure times, delays, line numbers, and destinations. *(Placeholder logic is used)*.

2.  **Data Processing (Python - `pandas`):**
    * Cleaned the fetched data.
    * Converted timestamp information into usable datetime objects.
    * Calculated delay durations.

3.  **Dashboard Application (Python - `streamlit`):**
    * Built a simple web application (`app.py`) using Streamlit.
    * The app allows a user (hypothetically) to select a station.
    * It calls the data fetching script (or loads sample data).
    * Displays upcoming departures in a table format.
    * Shows basic statistics on current delays.
    * Includes a placeholder for potential visualizations (e.g., a bar chart of delays by line).

4.  **Data Storage (Placeholder):**
    * For demonstration, the processed data might be temporarily stored or passed directly to Streamlit. A real application might use a simple database or file caching.

## Potential Findings (Example)

* Identification of frequently delayed lines or times of day based on sampled data.
* Visualization of real-time departure boards for user-selected stations.
* (Further findings would depend on the actual data retrieved).

## How to Run

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd berlin-transport-dashboard
    ```
2.  **Set up Python environment:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **(API Setup - If Implementing Fully):** Obtain necessary API credentials from VBB and update placeholder variables in `vbb_data_fetcher.py`.
4.  **Run the Streamlit App:**
    ```bash
    streamlit run app.py
    ```
    This will start the web application locally, typically opening it in your browser.

## Tools Used

* **Python:** Pandas, Requests, Streamlit, Datetime
* **Jupyter Notebook** (for initial exploration, optional)
* **VBB API** (conceptual data source)
