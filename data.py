import pandas as pd
import numpy as np
import datetime
import random

# This function create sample data if user don't enter any CSV file.


def make_sample_data():

    rows = []
    random.seed(42)

    for i in range(2000):

        day = random.randint(1, 5)

        hour = random.randint(8, 20)
        minute = random.randint(0, 59)

        location = random.choice(
            ["Library", "Cafeteria", "Lab", "Auditorium", "Classroom"]
        )
        device = random.choice(["iPhone", "Android", "Laptop", "Tablet", "MacBook"])

        download = round(random.uniform(1, 100), 2)
        upload = round(random.uniform(0.5, 50), 2)
        signal = random.randint(-90, -30)
        networks = random.randint(1, 20)
        num_devices = random.randint(1, 50)
        mac_or_pc = random.choice(["Mac", "PC"])

        rows.append(
            [
                datetime.date(2026, 3, day),
                datetime.time(hour, minute),
                device,
                location,
                download,
                upload,
                signal,
                networks,
                num_devices,
                mac_or_pc,
            ]
        )

    column_names = [
        "Date",
        "Time",
        "Device",
        "Location",
        "SpeedDownload",
        "SpeedUpload",
        "StrengthStrongest",
        "NumberofAvailableNetworks",
        "NumberOfDevices",
        "MacOrPC",
    ]

    df = pd.DataFrame(rows, columns=column_names)
    return df


# This function guesses which clos are matched to user CSV file.


def guess_columns(column_list):

    guesses = {}

    date_keywords = [
        "connection_time",
        "connectiontime",
        "connect",
        "start",
        "login",
        "date",
        "day",
        "timestamp",
        "datetime",
    ]

    time_keywords = ["time", "hour", "clock"]

    location_keywords = [
        "location",
        "loc",
        "building",
        "zone",
        "area",
        "place",
        "site",
        "venue",
    ]

    device_keywords = [
        "user_id",
        "userid",
        "user",
        "device_id",
        "deviceid",
        "device",
        "mac",
        "client",
        "host",
        "station",
    ]

    download_keywords = [
        "speeddownload",
        "download",
        "down",
        "data_used",
        "dataused",
        "datausedmb",
        "speed",
        "data",
        "mb",
        "bytes",
        "rx",
    ]

    upload_keywords = ["speedupload", "upload", "up", "tx"]

    signal_keywords = [
        "strengthstrongest",
        "strength",
        "signal",
        "rssi",
        "dbm",
        "power",
    ]

    networks_keywords = [
        "numberofavailablenetworks",
        "availablenetworks",
        "network",
        "available",
        "ssid",
    ]

    ndevices_keywords = [
        "numberofdevices",
        "numdevices",
        "numdevice",
        "connected",
        "clients",
    ]

    ap_keywords = [
        "access_point",
        "accesspoint",
        "access",
        "ap",
        "bssid",
        "router",
        "node",
    ]

    disconnection_keywords = [
        "disconnection_time",
        "disconnectiontime",
        "disconnect",
        "end",
        "logout",
        "finish",
    ]

    for col in column_list:
        col_lower = col.lower().replace(" ", "").replace("_", "")

        for word in date_keywords:
            word_clean = word.replace("_", "")
            if word_clean in col_lower and "col_date" not in guesses:
                guesses["col_date"] = col

        for word in time_keywords:
            if word in col_lower and "col_time" not in guesses:
                # It checks that we don't pick connection_time column.
                if "connection" not in col_lower and "disconnection" not in col_lower:
                    guesses["col_time"] = col

        for word in location_keywords:
            if word in col_lower and "col_location" not in guesses:
                guesses["col_location"] = col

        for word in device_keywords:
            word_clean = word.replace("_", "")
            if word_clean in col_lower and "col_device" not in guesses:
                guesses["col_device"] = col

        for word in download_keywords:
            word_clean = word.replace("_", "")
            if word_clean in col_lower and "col_download" not in guesses:
                guesses["col_download"] = col

        for word in upload_keywords:
            if word in col_lower and "col_upload" not in guesses:
                guesses["col_upload"] = col

        for word in signal_keywords:
            if word in col_lower and "col_signal" not in guesses:
                guesses["col_signal"] = col

        for word in networks_keywords:
            word_clean = word.replace("_", "")
            if word_clean in col_lower and "col_networks" not in guesses:
                guesses["col_networks"] = col

        for word in ndevices_keywords:
            word_clean = word.replace("_", "")
            if word_clean in col_lower and "col_numdevices" not in guesses:
                guesses["col_numdevices"] = col

        for word in ap_keywords:
            word_clean = word.replace("_", "")
            if word_clean in col_lower and "col_ap" not in guesses:
                guesses["col_ap"] = col

        for word in disconnection_keywords:
            word_clean = word.replace("_", "")
            if word_clean in col_lower and "col_disconnection" not in guesses:
                guesses["col_disconnection"] = col

    return guesses


# This function combines date and time into a dataframe.
def add_datetime_column(df, date_col, time_col):

    try:
        if time_col is not None and time_col in df.columns:
            combined = df[date_col].astype(str) + " " + df[time_col].astype(str)
        else:
            combined = df[date_col].astype(str)

        try:
            df["_datetime"] = pd.to_datetime(combined, dayfirst=False)
        except Exception:

            try:
                df["_datetime"] = pd.to_datetime(combined, dayfirst=True)
            except Exception:

                df["_datetime"] = pd.to_datetime(combined, infer_datetime_format=True)

        # Here hours are extracted from the dataframe.
        df["_hour"] = df["_datetime"].dt.hour

        return df, None

    except Exception as error:
        return df, str(error)


# This function cleans the dataset by removing duplicates and  empty or nonsense values changed with unknown.


def clean_text_columns(df, column_list):

    invalid_values = [
        "nan",
        "none",
        "null",
        "na",
        "n/a",
        "a lot",
        "unknown",
        "",
        " ",
        "-",
        "?",
    ]

    for col in column_list:
        if col is not None and col in df.columns:

            df[col] = df[col].astype(str).str.strip()

            df[col] = df[col].apply(
                lambda val: "Unknown" if str(val).lower() in invalid_values else val
            )
            df[col] = df[col].apply(
                lambda val: str(val).capitalize() if val != "Unknown" else val
            )

    return df


# This function confirms that there are only numbers in the number cols because sometimes they store they store text.


def convert_to_numbers(df, column_list):

    for col in column_list:
        if col is not None and col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


# This function filter the data for selected cols by user.


def apply_filters(df, location_col, selected_locations, hour_start, hour_end):

    location_filter = df[location_col].isin(selected_locations)
    hour_filter = df["_hour"].between(hour_start, hour_end)
    filtered = df[location_filter & hour_filter].copy()

    return filtered


# This function cleans the whole data set and returns a report of what was cleaned.


def clean_full_dataset(df, location_col, device_col, numeric_cols):

    report = []

    total_rows_before = len(df)

    empty_rows = df.isnull().all(axis=1).sum()
    if empty_rows > 0:
        df = df.dropna(how="all")
        report.append("Removed " + str(empty_rows) + " completely empty rows")

    duplicates = df.duplicated().sum()
    if duplicates > 0:
        df = df.drop_duplicates()
        report.append("Removed " + str(duplicates) + " duplicate rows")
    else:
        report.append("No duplicate rows found")

    invalid_values = ["nan", "none", "null", "na", "n/a", "a lot", "", " ", "-", "?"]

    text_cols = [location_col, device_col]

    for col in text_cols:
        if col is not None and col in df.columns:

            invalid_count = (
                df[col].astype(str).str.strip().str.lower().isin(invalid_values).sum()
            )

            df[col] = df[col].astype(str).str.strip()

            # fixed - converts to string first so float NaN never crashes
            df[col] = df[col].apply(
                lambda val: "Unknown" if str(val).lower() in invalid_values else val
            )

            df[col] = df[col].apply(
                lambda val: str(val).capitalize() if val != "Unknown" else val
            )

            if invalid_count > 0:
                report.append(
                    "Fixed "
                    + str(invalid_count)
                    + " empty or invalid values in '"
                    + col
                    + "' column → replaced with 'Unknown'"
                )
            else:
                report.append("No invalid values found in '" + col + "' column")

    for col in numeric_cols:
        if col is not None and col in df.columns:

            non_numeric = pd.to_numeric(df[col], errors="coerce").isnull().sum()
            original_nulls = df[col].isnull().sum()
            bad_values = non_numeric - original_nulls

            df[col] = pd.to_numeric(df[col], errors="coerce")

            if bad_values > 0:
                report.append(
                    "Fixed "
                    + str(bad_values)
                    + " non-numeric values in '"
                    + col
                    + "' column"
                )

            missing_nums = df[col].isnull().sum()
            if missing_nums > 0:
                report.append(
                    "Found "
                    + str(missing_nums)
                    + " missing values in '"
                    + col
                    + "' column (shown as empty in charts)"
                )

    if location_col and location_col in df.columns:
        missing_location = df[location_col].isnull().sum()
        empty_location = (df[location_col].astype(str).str.strip() == "").sum()
        total_bad_location = missing_location + empty_location

        if total_bad_location > 0:
            df = df[df[location_col].notna()]
            df = df[df[location_col].astype(str).str.strip() != ""]
            report.append(
                "Removed " + str(total_bad_location) + " rows with missing location"
            )
        else:
            report.append("All rows have a valid location")
    if location_col and location_col in df.columns:
        before_locs = df[location_col].nunique()
        df["_loc_clean"] = df[location_col].str.replace(" ", "").str.lower()
        mapping = {}
        for orig, clean in zip(df[location_col], df["_loc_clean"]):
            if clean not in mapping:
                mapping[clean] = orig
        df[location_col] = df["_loc_clean"].map(mapping)
        df = df.drop(columns=["_loc_clean"])
        after_locs = df[location_col].nunique()
        if before_locs != after_locs:
            report.append(
                "Merged " + str(before_locs - after_locs) + " duplicate location names"
            )

    # Final summary of the dataset.

    total_rows_after = len(df)
    rows_removed = total_rows_before - total_rows_after

    summary = {
        "rows_before": total_rows_before,
        "rows_after": total_rows_after,
        "rows_removed": rows_removed,
        "report": report,
    }

    return df, summary


# This function calculate the session time (means how much time a device connected to router).


def calculate_session_duration(df, connection_col, disconnection_col):

    try:
        conn_time = pd.to_datetime(df[connection_col])
        disconn_time = pd.to_datetime(df[disconnection_col])

        df["_duration_min"] = (disconn_time - conn_time).dt.total_seconds() / 60

        df.loc[df["_duration_min"] < 0, "_duration_min"] = None

        return df, None

    except Exception as error:
        return df, str(error)


def get_user_type(user_id):

    # This function identify the user type from ID.

    user_id = str(user_id).strip()

    if user_id.startswith("U") or user_id.startswith("u"):
        return "Registered User"
    elif user_id.startswith("D") or user_id.startswith("d"):
        return "Registered Device"
    elif user_id.lower() in ["nan", "none", "unknown", ""]:
        return "Unknown"
    else:
        return user_id
