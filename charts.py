import matplotlib.pyplot as plt

MAIN_COLOR = "#cbd5e1"
HIGHLIGHT = "#2563eb"
BG_COLOR = "#ffffff"
TEXT_COLOR = "#334155"
GRID_COLOR = "#f1f5f9"
IS_DARK_MODE = False

def set_theme(is_dark):
    """Dynamically updates all chart colors based on the sidebar toggle."""
    global MAIN_COLOR, HIGHLIGHT, BG_COLOR, TEXT_COLOR, GRID_COLOR, IS_DARK_MODE
    IS_DARK_MODE = is_dark
    
    if is_dark:
        MAIN_COLOR = "#334155"
        HIGHLIGHT = "#6ce2f7"
        BG_COLOR = "#0f172a"
        TEXT_COLOR = "#94a3b8"
        GRID_COLOR = "#1e293b"
        plt.rcParams["figure.facecolor"] = "#0f172a"
        plt.rcParams["axes.facecolor"] = "#0f172a"
        plt.rcParams["text.color"] = "#f8fafc"
    else:
        MAIN_COLOR = "#cbd5e1"
        HIGHLIGHT = "#2563eb"
        BG_COLOR = "#ffffff"
        TEXT_COLOR = "#334155"
        GRID_COLOR = "#f1f5f9"
        plt.rcParams["figure.facecolor"] = "#f8fafc"
        plt.rcParams["axes.facecolor"] = "#ffffff"
        plt.rcParams["text.color"] = "#334155"
        
    plt.rcParams["axes.edgecolor"] = GRID_COLOR
    plt.rcParams["axes.labelcolor"] = TEXT_COLOR
    plt.rcParams["xtick.color"] = TEXT_COLOR
    plt.rcParams["ytick.color"] = TEXT_COLOR
    plt.rcParams["grid.color"] = GRID_COLOR
    plt.rcParams["grid.linewidth"] = 0.6
    plt.rcParams["font.family"] = "sans-serif"


def remove_top_right_borders(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(GRID_COLOR)
    ax.spines["bottom"].set_color(GRID_COLOR)


def get_chart_height(num_items):
    return max(4, num_items * 0.4)


def get_font_size(num_items):
    if num_items > 20:
        return 7
    elif num_items > 10:
        return 9
    else:
        return 11


def make_hour_chart(df):
    hour_counts = df["_hour"].value_counts().sort_index()
    all_hours = list(range(24))
    hour_counts = hour_counts.reindex(all_hours, fill_value=0)
    busiest_hour = hour_counts.idxmax()
    colors = []
    for h in all_hours:
        if h == busiest_hour:
            colors.append(HIGHLIGHT)
        else:
            colors.append(MAIN_COLOR)

    # draw the chart
    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.bar(all_hours, hour_counts.values, color=colors, width=0.7)
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Number of Connections")
    ax.set_xticks(range(0, 24, 2))
    ax.grid(axis="y", alpha=0.5)
    remove_top_right_borders(ax)
    fig.tight_layout()
    return fig


def make_location_chart(df, location_col):
    location_counts = df[location_col].value_counts()
    num_locations = len(location_counts)
    location_counts = location_counts.sort_values(ascending=True)
    max_value = location_counts.max()
    highlighted = False
    colors = []
    for count in location_counts.values:
        if count == max_value and not highlighted:
            colors.append(HIGHLIGHT)
            highlighted = True
        else:
            colors.append(MAIN_COLOR)

    chart_height = get_chart_height(num_locations)
    font_size = get_font_size(num_locations)

    # draw horizontal bar chart so location names fit on left side
    fig, ax = plt.subplots(figsize=(10, chart_height))
    ax.barh(location_counts.index, location_counts.values,
            color=colors, height=0.6)
    ax.set_xlabel("Number of Records")
    ax.tick_params(axis="y", labelsize=font_size)
    ax.tick_params(axis="x", labelsize=font_size)
    ax.grid(axis="x", alpha=0.5)
    remove_top_right_borders(ax)
    fig.tight_layout(pad=1.5)

    return fig


def make_download_chart(df, location_col, download_col):
    avg_speed = df.groupby(location_col)[download_col].mean()
    avg_speed = avg_speed.sort_values(ascending=False)
    # sort ascending so highest bar appears at bottom (most visible)
    avg_speed = avg_speed.sort_values(ascending=True)
    num_locations = len(avg_speed)

    # highlight only the bar with the highest value
    max_val = avg_speed.max()
    highlighted = False
    colors = []
    for val in avg_speed.values:
        if val == max_val and not highlighted:
            colors.append(HIGHLIGHT)
            highlighted = True
        else:
            colors.append(MAIN_COLOR)

    chart_height = get_chart_height(num_locations)
    font_size = get_font_size(num_locations)

    fig, ax = plt.subplots(figsize=(7, chart_height))
    ax.barh(avg_speed.index, avg_speed.values, color=colors, height=0.6)
    ax.set_xlabel("Mbps")
    ax.tick_params(axis="y", labelsize=font_size)
    ax.tick_params(axis="x", labelsize=font_size)
    ax.grid(axis="x", alpha=0.5)
    remove_top_right_borders(ax)
    fig.tight_layout(pad=1.5)

    return fig


def make_signal_chart(df, location_col, signal_col):
    avg_signal = df.groupby(location_col)[signal_col].mean()
    avg_signal = avg_signal.sort_values(ascending=True)
    num_locations = len(avg_signal)
    max_val = avg_signal.max()
    highlighted = False
    colors = []
    for val in avg_signal.values:
        if val == max_val and not highlighted:
            colors.append(HIGHLIGHT)
            highlighted = True
        else:
            colors.append(MAIN_COLOR)

    chart_height = get_chart_height(num_locations)
    font_size = get_font_size(num_locations)

    fig, ax = plt.subplots(figsize=(7, chart_height))
    ax.barh(avg_signal.index, avg_signal.values, color=colors, height=0.6)
    ax.set_xlabel("Signal Strength (dBm)")
    ax.tick_params(axis="y", labelsize=font_size)
    ax.tick_params(axis="x", labelsize=font_size)
    ax.grid(axis="x", alpha=0.5)
    remove_top_right_borders(ax)
    fig.tight_layout(pad=1.5)

    return fig


def make_upload_chart(df, upload_col):
    upload_values = df[upload_col].dropna()
    def get_speed_group(speed):
        if speed <= 25:
            return "0-25 Mbps (Very Slow)"
        elif speed <= 50:
            return "25-50 Mbps (Slow)"
        elif speed <= 75:
            return "50-75 Mbps (Medium)"
        elif speed <= 100:
            return "75-100 Mbps (Fast)"
        elif speed <= 150:
            return "100-150 Mbps (Very Fast)"
        else:
            return "150+ Mbps (Excellent)"

    speed_groups = upload_values.apply(get_speed_group)

    # count how many records are in each group
    group_order = [
        "0-25 Mbps (Very Slow)",
        "25-50 Mbps (Slow)",
        "50-75 Mbps (Medium)",
        "75-100 Mbps (Fast)",
        "100-150 Mbps (Very Fast)",
        "150+ Mbps (Excellent)"
    ]
    group_counts = speed_groups.value_counts().reindex(group_order, fill_value=0)

    if IS_DARK_MODE:
        bar_colors = ["#207c9e", "#12a3cf", "#07b7e7", "#12c7f5", "#43e3ff", "#87ecfc"]
    else:
        bar_colors = ["#b1d3fc", "#93c5fd", "#60a5fa", "#3b82f6", "#2563eb", "#1d4ed8"]

    # draw the chart
    fig, ax = plt.subplots(figsize=(9, 4))
    bars = ax.barh(group_counts.index, group_counts.values,
                   color=bar_colors, height=0.6)

    for bar in bars:
        width = bar.get_width()
        if width > 0:
            ax.text(
                width + 0.1,
                bar.get_y() + bar.get_height() / 2,
                str(int(width)),
                va="center",
                fontsize=9,
                color=TEXT_COLOR
            )

    ax.set_xlabel("Number of Records")
    ax.set_title("Upload Speed Distribution", fontsize=11, pad=10)
    ax.grid(axis="x", alpha=0.4)
    remove_top_right_borders(ax)
    fig.tight_layout(pad=1.5)

    return fig


def make_networks_chart(df, networks_col):
    network_values = df[networks_col].dropna()
    def get_network_group(n):
        if n <= 3:
            return "1-3 networks"
        elif n <= 6:
            return "4-6 networks"
        elif n <= 10:
            return "7-10 networks"
        elif n <= 15:
            return "11-15 networks"
        else:
            return "16+ networks"

    network_groups = network_values.apply(get_network_group)

    group_order = [
        "1-3 networks",
        "4-6 networks",
        "7-10 networks",
        "11-15 networks",
        "16+ networks"
    ]

    group_counts = network_groups.value_counts().reindex(group_order, fill_value=0)

    if IS_DARK_MODE:
        bar_colors = ["#207c9e", "#12a3cf", "#07b7e7", "#12c7f5", "#43e3ff", "#87ecfc"]
    else:
        bar_colors = ["#b1d3fc", "#93c5fd", "#60a5fa", "#3b82f6", "#2563eb", "#1d4ed8"]

    fig, ax = plt.subplots(figsize=(9, 4))
    bars = ax.barh(group_counts.index, group_counts.values,
                   color=bar_colors, height=0.5)

    for bar in bars:
        width = bar.get_width()
        if width > 0:
            ax.text(
                width + 0.1,
                bar.get_y() + bar.get_height() / 2,
                str(int(width)),
                va="center",
                fontsize=9,
                color=TEXT_COLOR
            )

    ax.set_xlabel("Number of Records")
    ax.set_title("Available Networks Distribution", fontsize=11, pad=10)
    ax.grid(axis="x", alpha=0.4)
    remove_top_right_borders(ax)
    fig.tight_layout(pad=1.5)

    return fig


def make_device_chart(df, device_col):
    device_counts = df[device_col].value_counts().head(10)
    num_devices = len(device_counts)

    colors = []
    for i in range(len(device_counts)):
        if i == 0:
            colors.append(HIGHLIGHT)
        else:
            colors.append(MAIN_COLOR)

    chart_height = get_chart_height(num_devices)
    font_size = get_font_size(num_devices)

    fig, ax = plt.subplots(figsize=(10, chart_height))
    ax.barh(device_counts.index, device_counts.values, color=colors, height=0.5)
    ax.set_xlabel("Number of Records")
    ax.tick_params(axis="y", labelsize=font_size)
    ax.tick_params(axis="x", labelsize=font_size)
    ax.grid(axis="x", alpha=0.5)
    remove_top_right_borders(ax)
    fig.tight_layout(pad=1.5)

    return fig


def make_duration_chart(df):
    duration_values = df["_duration_min"].dropna()
    def get_duration_group(mins):
        if mins <= 30:
            return "0-30 min (Very Short)"
        elif mins <= 60:
            return "30-60 min (Short)"
        elif mins <= 90:
            return "60-90 min (Medium)"
        elif mins <= 120:
            return "90-120 min (Long)"
        else:
            return "120+ min (Very Long)"

    duration_groups = duration_values.apply(get_duration_group)

    group_order = [
        "0-30 min (Very Short)",
        "30-60 min (Short)",
        "60-90 min (Medium)",
        "90-120 min (Long)",
        "120+ min (Very Long)"
    ]

    group_counts = duration_groups.value_counts().reindex(group_order, fill_value=0)

    if IS_DARK_MODE:
        bar_colors = ["#207c9e", "#12a3cf", "#07b7e7", "#12c7f5", "#43e3ff", "#87ecfc"]
    else:
        bar_colors = ["#b1d3fc", "#93c5fd", "#60a5fa", "#3b82f6", "#2563eb", "#1d4ed8"]


    fig, ax = plt.subplots(figsize=(9, 4))
    bars = ax.barh(group_counts.index, group_counts.values,
                   color=bar_colors, height=0.5)

    # add count number at end of each bar
    for bar in bars:
        width = bar.get_width()
        if width > 0:
            ax.text(
                width + 0.5,
                bar.get_y() + bar.get_height() / 2,
                str(int(width)),
                va="center",
                fontsize=9,
                color="#555555"
            )

    ax.set_xlabel("Number of Sessions")
    ax.set_title("How Long Do Users Stay Connected?", fontsize=11, pad=10)
    ax.grid(axis="x", alpha=0.4)
    remove_top_right_borders(ax)
    fig.tight_layout(pad=1.5)

    return fig
