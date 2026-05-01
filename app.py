import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import data
import charts

st.set_page_config(page_title="University WiFi Analytics", layout="wide")

import streamlit as st

# --- Theme Switcher ---
dark_mode_enabled = st.sidebar.toggle("🌙 Dark Mode", value=True)

# === DARK MODE THEME ===
dark_theme_css = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
  html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }

  :root {
    --bg-main: #0f172a;
    --bg-sidebar: #020617;
    --accent: #06b6d4;
    --text-primary: #f8fafc;
    --border: #334155;
  }

  /* Main Backgrounds */
  [data-testid="stAppViewContainer"] {
    background-color: var(--bg-main);
    color: var(--text-primary);
  }
  [data-testid="stSidebar"] {
    background-color: var(--bg-sidebar);
  }
  /* Sidebar Text Color */
[data-testid="stSidebar"] * {
  color: #ffffff !important;
}

  [data-testid="stHeader"] {
    background-color: transparent;
  }

  /* Metric Cards */
  [data-testid="stMetric"] {
    background-color: #1e293b;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 15px 20px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.5);
    transition: all 0.3s ease-in-out;
  }
  [data-testid="stMetric"]:hover {
    transform: translateY(-3px);
  }
  [data-testid="stMetricValue"] {
    color: var(--accent);
    font-size: 1.9rem;
    font-weight: 600;
  }
  [data-testid="stMetricLabel"] {
    color: #94a3b8;
  }

  /* File Upload */
  [data-testid="stFileUploadDropzone"] {
    background-color: var(--bg-main);
    border: 2px dashed var(--border);
    color: var(--text-primary);
  }

  /* Dropdowns & Select Boxes */
  div[data-baseweb="select"] > div {
    background-color: var(--bg-main);
    border-color: var(--border);
    color: var(--text-primary);
  }
  div[data-baseweb="popover"] div {
    background-color: var(--bg-sidebar);
    color: #cbd5e1;
  }

  /* Multiselect Tags */
  span[data-baseweb="tag"] {
    background-color: #164e63;
    color: var(--accent);
  }

  /* Slider */
  div[data-baseweb="slider"] div[data-testid="stTickBar"] > div {
    background-color: var(--accent);
  }
  div[data-baseweb="slider"] div[role="slider"] {
    background-color: var(--accent);
  }

  /* Buttons */
  .stDownloadButton button {
    background-color: var(--accent);
    color: var(--bg-sidebar);
    font-weight: 600;
    border: none;
    border-radius: 6px;
    transition: background 0.3s ease;
  }
  .stDownloadButton button:hover {
    background-color: #0891b2;
  }

  hr { border-top: 1px solid var(--border); }

  /* Hide Default Streamlit Menu */
  #MainMenu {visibility: hidden;}
  footer {visibility: hidden;}
</style>
"""

# === LIGHT MODE THEME ===
light_theme_css = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
  html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }

  :root {
    --bg-main: #f8fafc;
    --bg-sidebar: #f1f5f9;
    --accent: #2563eb;
    --text-primary: #334155;
    --border: #cbd5e1;
  }

  /* Main Backgrounds */
  [data-testid="stAppViewContainer"] {
    background-color: var(--bg-main);
    color: var(--text-primary);
  }
  [data-testid="stSidebar"] {
    background-color: var(--bg-sidebar);
    color: var(--text-primary);
  }
  [data-testid="stHeader"] {
    background-color: transparent;
  }

  /* Metric Cards */
  [data-testid="stMetric"] {
    background-color: #ffffff;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 15px 20px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    transition: all 0.3s ease-in-out;
  }
  [data-testid="stMetric"]:hover {
    transform: translateY(-3px);
  }
  [data-testid="stMetricValue"] {
    color: var(--accent);
    font-size: 1.9rem;
    font-weight: 600;
  }
  [data-testid="stMetricLabel"] {
    color: #64748b;
  }

  /* File Upload */
  [data-testid="stFileUploadDropzone"] {
    background-color: #ffffff;
    border: 2px dashed var(--border);
    color: var(--text-primary);
  }

  /* Dropdowns & Select Boxes */
  div[data-baseweb="select"] > div {
    background-color: #ffffff;
    border-color: var(--border);
    color: var(--text-primary);
  }
  div[data-baseweb="popover"] div {
    background-color: #ffffff;
    color: var(--text-primary);
  }

  /* Multiselect Tags */
  span[data-baseweb="tag"] {
    background-color: #bfdbfe;
    color: var(--accent);
  }

  /* Slider */
  div[data-baseweb="slider"] div[data-testid="stTickBar"] > div {
    background-color: var(--accent);
  }
  div[data-baseweb="slider"] div[role="slider"] {
    background-color: var(--accent);
  }

  /* Buttons */
  .stDownloadButton button {
    background-color: var(--accent);
    color: #ffffff;
    font-weight: 600;
    border: none;
    border-radius: 6px;
    transition: background 0.3s ease;
  }
  .stDownloadButton button:hover {
    background-color: #1e40af;
  }

  hr { border-top: 1px solid var(--border); }

  /* Hide Default Streamlit Menu */
  #MainMenu {visibility: hidden;}
  footer {visibility: hidden;}
</style>
"""

# Apply theme
if dark_mode_enabled:
    st.markdown(dark_theme_css, unsafe_allow_html=True)
else:
    st.markdown(light_theme_css, unsafe_allow_html=True)


st.sidebar.title("WiFi Analytics")
st.sidebar.markdown("---")

uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    raw_data = pd.read_csv(uploaded_file)
    auto_guesses = data.guess_columns(raw_data.columns.tolist())

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Match Your Columns**")
    st.sidebar.caption("We tried to auto-detect. Please fix if wrong.")

    all_columns = ["-- select --"] + raw_data.columns.tolist()

    def get_index(role_key):
        guessed_col = auto_guesses.get(role_key)
        if guessed_col in all_columns:
            return all_columns.index(guessed_col)
        return 0

# Making a drop down list for each col.
    st.sidebar.markdown("**Required Columns**")

    col_date = st.sidebar.selectbox(
        "Date or Connection Time column",
        all_columns,
        index=get_index("col_date"),
        key="col_date",
        help="Pick the column that has the date or connection time",
    )

    col_location = st.sidebar.selectbox(
        "Location column",
        all_columns,
        index=get_index("col_location"),
        key="col_location",
        help="Pick the column that has the location or building name",
    )

    col_device = st.sidebar.selectbox(
        "Device or User ID column",
        all_columns,
        index=get_index("col_device"),
        key="col_device",
        help="Pick the column that has the device name or user ID",
    )

    st.sidebar.markdown("**Optional Columns**")

    col_time = st.sidebar.selectbox(
        "Time column (only if date and time are separate)",
        all_columns,
        index=get_index("col_time"),
        key="col_time",
        help="Only pick this if your date and time are in different columns",
    )

    col_disconnection = st.sidebar.selectbox(
        "Disconnection Time column",
        all_columns,
        index=get_index("col_disconnection"),
        key="col_disconnection",
        help="Pick the column that has the disconnection or end time (wifi_sample.csv)",
    )

    col_ap = st.sidebar.selectbox(
        "Access Point column",
        all_columns,
        index=get_index("col_ap"),
        key="col_ap",
        help="Pick the column that has the access point or router name (wifi_sample.csv)",
    )

    col_download = st.sidebar.selectbox(
        "Download speed or Data Used column",
        all_columns,
        index=get_index("col_download"),
        key="col_download",
        help="Pick the column that has download speed or data usage in MB",
    )

    col_upload = st.sidebar.selectbox(
        "Upload speed column",
        all_columns,
        index=get_index("col_upload"),
        key="col_upload",
        help="Pick the column that has upload speed",
    )

    col_signal = st.sidebar.selectbox(
        "Signal strength column",
        all_columns,
        index=get_index("col_signal"),
        key="col_signal",
        help="Pick the column that has wifi signal strength",
    )

    col_networks = st.sidebar.selectbox(
        "Available networks column",
        all_columns,
        index=get_index("col_networks"),
        key="col_networks",
        help="Pick the column that has number of available networks",
    )

    col_ndevices = st.sidebar.selectbox(
        "Number of devices column",
        all_columns,
        index=get_index("col_numdevices"),
        key="col_numdevices",
        help="Pick the column that has number of connected devices",
    )

    missing_cols = []

    if col_date == "-- select --":
        missing_cols.append("Date or Connection Time")

    if col_location == "-- select --":
        missing_cols.append("Location")

    if col_device == "-- select --":
        missing_cols.append("Device or User ID")

    if len(missing_cols) > 0:
        st.sidebar.error("Please select: " + ", ".join(missing_cols))
        st.warning("Please map the required columns in the sidebar to continue.")
        st.stop()

    time_col = col_time if col_time != "-- select --" else None

    df, error_msg = data.add_datetime_column(raw_data.copy(), col_date, time_col)

    if error_msg:
        st.error("Could not read the date column. Error: " + error_msg)
        st.stop()

    location_col = col_location
    device_col = col_device
    download_col = col_download if col_download != "-- select --" else None
    upload_col = col_upload if col_upload != "-- select --" else None
    signal_col = col_signal if col_signal != "-- select --" else None
    networks_col = col_networks if col_networks != "-- select --" else None
    ndevices_col = col_ndevices if col_ndevices != "-- select --" else None
    ap_col = col_ap if col_ap != "-- select --" else None
    disconnection_col = (
        col_disconnection if col_disconnection != "-- select --" else None
    )

    df, cleaning_summary = data.clean_full_dataset(
        df,
        location_col,
        device_col,
        [download_col, upload_col, signal_col, networks_col, ndevices_col],
    )

    st.sidebar.success("File loaded! " + str(len(df)) + " rows found.")

else:
    df = data.make_sample_data()

    df, error_msg = data.add_datetime_column(df, "Date", "Time")

    location_col = "Location"
    device_col = "Device"
    download_col = "SpeedDownload"
    upload_col = "SpeedUpload"
    signal_col = "StrengthStrongest"
    networks_col = "NumberofAvailableNetworks"
    ndevices_col = "NumberOfDevices"
    ap_col = None
    disconnection_col = None

    st.sidebar.info("No file uploaded. Showing sample data.")

    cleaning_summary = None

if disconnection_col and disconnection_col in df.columns:
    df, dur_error = data.calculate_session_duration(
        df,
        "_datetime" if "_datetime" in df.columns else df.columns[0],
        disconnection_col,
    )
    if dur_error:
        st.warning("Could not calculate session duration: " + dur_error)

st.sidebar.markdown("---")
st.sidebar.download_button(
    label="Download CSV",
    data=df.to_csv(index=False),
    file_name="wifi_data.csv",
    mime="text/csv",
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Filters**")

all_locations = sorted(df[location_col].dropna().unique().tolist())

selected_locations = st.sidebar.multiselect(
    "Select Locations", all_locations, default=all_locations
)

selected_hours = st.sidebar.slider("Hour Range", 0, 23, (0, 23))

filtered_df = data.apply_filters(
    df, location_col, selected_locations, selected_hours[0], selected_hours[1]
)

if filtered_df.empty:
    st.warning("No data found with current filters. Try changing them.")
    st.stop()

st.title("University WiFi Usage Dashboard")
st.write(
    "Showing " + str(len(filtered_df)) + " records out of " + str(len(df)) + " total"
)
st.markdown("---")


# data cleaning summary.

if cleaning_summary is not None:

    st.subheader("Data Cleaning Report")

    clean_col1, clean_col2, clean_col3 = st.columns(3)
    clean_col1.metric("Rows Before Cleaning", str(cleaning_summary["rows_before"]))
    clean_col2.metric("Rows After Cleaning", str(cleaning_summary["rows_after"]))
    clean_col3.metric("Rows Removed", str(cleaning_summary["rows_removed"]))

    st.markdown("**What was cleaned:**")
    for step in cleaning_summary["report"]:

        if "No " in step or "found" not in step.lower():
            st.success("✔ " + step)
        else:
            st.warning("⚠ " + step)

    st.markdown("---")


card1, card2, card3, card4 = st.columns(4)

card1.metric("Total Records", str(len(filtered_df)))


device_unique_count = filtered_df[device_col].nunique()
total_rows = len(filtered_df)
is_unique_id_column = device_unique_count > (total_rows * 0.8)

if is_unique_id_column:
    card2.metric("Unique Users", str(device_unique_count))
else:
    card2.metric("Unique Devices", str(device_unique_count))

card3.metric("Unique Locations", str(filtered_df[location_col].nunique()))

if download_col and download_col in filtered_df.columns:
    average_download = round(filtered_df[download_col].mean(), 1)

    col_name_lower = download_col.lower().replace("_", "")
    if "dataused" in col_name_lower or "usedmb" in col_name_lower:
        card4.metric("Avg Data Used (MB)", str(average_download))
    elif "byte" in col_name_lower:
        card4.metric("Avg Data Used (Bytes)", str(average_download))
    elif "download" in col_name_lower or "speed" in col_name_lower:
        card4.metric("Avg Download (Mbps)", str(average_download))
    elif average_download > 200:
        card4.metric("Avg Data Used (MB)", str(average_download))
    else:
        card4.metric("Avg Download Speed", str(average_download))


elif signal_col and signal_col in filtered_df.columns:
    average_signal = round(filtered_df[signal_col].mean(), 1)
    card4.metric("Avg Signal (dBm)", str(average_signal))

else:
    card4.metric("Locations Selected", str(len(selected_locations)))

if "_duration_min" in filtered_df.columns:
    avg_duration = round(filtered_df["_duration_min"].dropna().mean(), 1)
    st.markdown("")
    dur_col1, dur_col2, dur_col3 = st.columns(3)
    dur_col1.metric("Avg Session Duration (min)", str(avg_duration))
    dur_col2.metric(
        "Shortest Session (min)",
        str(round(filtered_df["_duration_min"].dropna().min(), 1)),
    )
    dur_col3.metric(
        "Longest Session (min)",
        str(round(filtered_df["_duration_min"].dropna().max(), 1)),
    )

st.markdown("---")

# This chart shows how many connections during the every hour.

st.subheader("Connections by Hour")
hour_chart = charts.make_hour_chart(filtered_df)
st.pyplot(hour_chart, use_container_width=True)
plt.close(hour_chart)

st.markdown("---")

# This chart shows the connection location.
st.subheader("Connections by Location")
location_chart = charts.make_location_chart(filtered_df, location_col)
st.pyplot(location_chart, use_container_width=True)
plt.close(location_chart)

st.markdown("---")

# This chart shows download speed or data used depending on column name.
if download_col and download_col in filtered_df.columns:
    col_check = download_col.lower().replace("_", "")
    if "dataused" in col_check or "usedmb" in col_check:
        st.subheader("Avg Data Used by Location (MB)")
    else:
        st.subheader("Avg Download Speed by Location")
    dl_chart = charts.make_download_chart(filtered_df, location_col, download_col)
    st.pyplot(dl_chart, use_container_width=True)
    plt.close(dl_chart)

elif signal_col and signal_col in filtered_df.columns:
    st.subheader("Signal Strength by Location")
    sig_chart = charts.make_signal_chart(filtered_df, location_col, signal_col)
    st.pyplot(sig_chart, use_container_width=True)
    plt.close(sig_chart)

st.markdown("---")

#This chart shows for how much time the connection was established.
if "_duration_min" in filtered_df.columns:
    st.markdown("---")
    st.subheader("Session Duration Distribution")
    duration_chart = charts.make_duration_chart(filtered_df)
    st.pyplot(duration_chart, use_container_width=True)
    plt.close(duration_chart)

#This chart shows the upload speed.
if upload_col and upload_col in filtered_df.columns:
    st.subheader("Upload Speed Distribution")
    ul_chart = charts.make_upload_chart(filtered_df, upload_col)
    st.pyplot(ul_chart, use_container_width=True)
    plt.close(ul_chart)

elif networks_col and networks_col in filtered_df.columns:
    st.subheader("Networks Nearby Distribution")
    net_chart = charts.make_networks_chart(filtered_df, networks_col)
    st.pyplot(net_chart, use_container_width=True)
    plt.close(net_chart)

st.markdown("---")

# chart  ----- access point chart

if ap_col and ap_col in filtered_df.columns:
    st.subheader("Connections by Access Point")
    ap_chart = charts.make_device_chart(filtered_df, ap_col)
    st.pyplot(ap_chart, use_container_width=True)
    plt.close(ap_chart)
    st.markdown("---")

# chart  ----- device breakdown

st.markdown("---")
st.subheader("Device Breakdown")

device_unique_count = filtered_df[device_col].nunique()
total_rows = len(filtered_df)
is_unique_id_column = device_unique_count > (total_rows * 0.8)

if is_unique_id_column:

    # device col has not unique device but contain IDs that are always unique so in this case not show chart.
    st.info(
        "The device column contains unique user IDs like U0001, U0002 etc. "
        "A chart would not be useful here since every user appears only once. "
        "Total unique users: **" + str(device_unique_count) + "**"
    )
else:

    # show unique devices and how much.
    device_chart = charts.make_device_chart(filtered_df, device_col)
    st.pyplot(device_chart, use_container_width=True)
    plt.close(device_chart)

st.markdown("---")

# Your CSV data show in table.

st.subheader("Raw Data Table")

with st.expander("Click here to show or hide the data table"):
    st.dataframe(
        filtered_df.reset_index(drop=True), use_container_width=True, height=300
    )
