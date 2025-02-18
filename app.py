import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from streamlit_sortables import sort_items
from PIL import Image
import requests
from io import BytesIO

# Load Google Fonts dynamically
GOOGLE_FONTS = [
    "Roboto", "Open Sans", "Montserrat", "Lato", "Poppins", "Raleway", "Merriweather",
    "Oswald", "Nunito", "Playfair Display", "Quicksand", "Ubuntu", "Pacifico", "Caveat"
]

# Simulated 5G measurement data (replace with real data source)
def generate_data():
    return {
        "MCS": np.random.randint(0, 28),
        "SINR": np.random.uniform(-10, 30),
        "Throughput": np.random.uniform(10, 100),
        "BLER": np.random.uniform(0, 1),
        "Constellation": np.random.uniform(-1, 1, (100, 2))  # 100 sample points
    }

# UI Layout
st.set_page_config(page_title="5G RAN Dashboard", layout="wide")
st.title("📡 5G RAN Network Dashboard")
st.sidebar.header("🎨 Customize Your Dashboard")

# Custom Theme Settings
bg_color = st.sidebar.color_picker("Background Color", "#ffffff")
text_color = st.sidebar.color_picker("Text Color", "#000000")
sidebar_color = st.sidebar.color_picker("Sidebar Background", "#f8f9fa")
selected_font = st.sidebar.selectbox("Select Font", GOOGLE_FONTS)

# Apply Custom Styles
st.markdown(
    f"""
    <style>
        body {{
            background-color: {bg_color};
            color: {text_color};
            font-family: '{selected_font}', sans-serif;
        }}
        .sidebar .sidebar-content {{
            background-color: {sidebar_color};
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Available measurement options
measurements = ["MCS", "SINR", "Throughput", "BLER", "Constellation"]
plot_types = [
    "Line Chart",  # Time series data, trends over time
    "Gauge",  # Real-time metrics like SINR, Throughput, MCS
    "Scatter (for Constellation)",  # IQ diagram for signal quality
    "Bar Chart",  # Comparison of different measurements
    "Histogram",  # Distribution of values over a range
    "Heatmap",  # Signal interference, correlation matrices
    "Box Plot",  # Variability, outliers, quartiles
    "Stem Plot",  # Discrete signal representation
    "Polar Plot",  # Beamforming patterns, angle-of-arrival
    "Waterfall Plot",  # Spectrum over time (frequency vs. time vs. power)
    "Surface Plot",  # 3D visualization of network parameters
    "Spectrogram",  # Frequency content of a signal over time
    "CDF (Cumulative Distribution Function)",  # Statistical distribution of a metric
    "Empirical PDF (Probability Density Function)",  # Probability distribution estimation
    "Violin Plot",  # Similar to box plot, showing density
    "Parallel Coordinates Plot",  # Multidimensional data visualization
    "Radial Plot",  # Circular representation of different parameters
    "3D Scatter Plot",  # Multi-axis analysis of data
    "Stacked Area Chart",  # Aggregated trends of multiple variables
    "Bubble Chart",  # Enhanced scatter plot with size variation
    "Vector Field Plot",  # Visualization of directional data (e.g., MIMO vectors)
    "Sankey Diagram",  # Flow of data or signal paths
    "Chord Diagram",  # Relations between multiple categories
]

# Session state to store active plots
if "active_plots" not in st.session_state:
    st.session_state.active_plots = []

# Select measurement, plot type, and styling
selected_measurement = st.sidebar.selectbox("Select Measurement", measurements)
selected_plot_type = st.sidebar.selectbox("Select Plot Type", plot_types)
selected_color = st.sidebar.color_picker("Select Plot Color", "#1f77b4")
selected_line_width = st.sidebar.slider("Line Thickness", 1, 5, 2)
selected_marker_style = st.sidebar.selectbox("Marker Style", ["circle", "square", "diamond", "cross"])

# Button to add plot
if st.sidebar.button("➕ Add Plot"):
    st.session_state.active_plots.append({
        "measurement": selected_measurement, 
        "plot_type": selected_plot_type, 
        "color": selected_color,
        "line_width": selected_line_width,
        "marker_style": selected_marker_style
    })

# Button to clear all plots
if st.sidebar.button("🗑 Clear All Plots"):
    st.session_state.active_plots = []

# Drag-and-drop arrangement
if st.session_state.active_plots:
    sorted_items = sort_items(
        [f"{plot['measurement']} ({plot['plot_type']})" for plot in st.session_state.active_plots]
    )
    reordered_plots = [
        st.session_state.active_plots[[f"{plot['measurement']} ({plot['plot_type']})" for plot in st.session_state.active_plots].index(item)]
        for item in sorted_items
    ]
    st.session_state.active_plots = reordered_plots

# Generate and display plots in a grid layout
st.subheader("📈 Live 5G Measurements")
data = generate_data()
marker_dict = {"circle": "circle", "square": "square", "diamond": "diamond", "cross": "x"}

if st.session_state.active_plots:
    cols = st.columns(len(st.session_state.active_plots))  # Grid layout with dynamic columns

    for idx, plot in enumerate(st.session_state.active_plots):
        meas, plot_type, color, line_width, marker_style = plot["measurement"], plot["plot_type"], plot["color"], plot["line_width"], plot["marker_style"]

        with cols[idx]:  # Place each plot in a column
            if plot_type == "Line Chart":
                y_values = np.random.uniform(0, 100, 10)  # Simulating 10 time samples
                fig = go.Figure(go.Scatter(y=y_values, x=list(range(10)), mode='lines', name=meas, line=dict(color=color, width=line_width)))
                fig.update_layout(title=f"{meas} - Line Chart", xaxis_title="Time", yaxis_title="Value", paper_bgcolor=bg_color, font_color=text_color)
                st.plotly_chart(fig)

            elif plot_type == "Gauge":
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=data[meas],
                    title={"text": meas},
                    gauge={"axis": {"range": [0, 100] if meas != "BLER" else [0, 1]}, "bar": {"color": color}}
                ))
                fig.update_layout(paper_bgcolor=bg_color, font_color=text_color)
                st.plotly_chart(fig)

            elif plot_type == "Scatter (for Constellation)" and meas == "Constellation":
                fig = go.Figure(go.Scatter(
                    x=data["Constellation"][:, 0], 
                    y=data["Constellation"][:, 1], 
                    mode='markers', 
                    marker=dict(color=color, symbol=marker_dict[marker_style])
                ))
                fig.update_layout(title="Constellation Plot", xaxis_title="I", yaxis_title="Q", paper_bgcolor=bg_color, font_color=text_color)
                st.plotly_chart(fig)

# Auto-refresh every few seconds
st.sidebar.write("🔄 The data updates automatically every time you refresh.")
