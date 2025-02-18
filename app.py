import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from streamlit_sortables import sort_items

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
st.title("\U0001F4E1 5G RAN Network Dashboard")
st.sidebar.header("\U0001F3A8 Customize Your Dashboard")

# Available measurement options
measurements = ["MCS", "SINR", "Throughput", "BLER", "Constellation"]
plot_types = ["Line Chart", "Gauge", "Scatter (for Constellation)"]

# Session state to store active plots
if "active_plots" not in st.session_state:
    st.session_state.active_plots = []

# Select measurement, plot type, and styling
selected_measurement = st.sidebar.selectbox("Select Measurement", measurements)
selected_plot_type = st.sidebar.selectbox("Select Plot Type", plot_types)
selected_color = st.sidebar.color_picker("Select Plot Color", "#1f77b4")
selected_line_width = st.sidebar.slider("Line Thickness", 1, 5, 2)
selected_marker_style = st.sidebar.selectbox("Marker Style", ["circle", "square", "diamond", "cross"])
custom_title = st.sidebar.text_input("Enter Plot Title", f"{selected_measurement} Plot")
plot_size = st.sidebar.slider("Plot Size", 300, 900, 600)

# Button to add plot
if st.sidebar.button("\U0001F4E2 Add Plot"):
    st.session_state.active_plots.append({
        "measurement": selected_measurement, 
        "plot_type": selected_plot_type, 
        "color": selected_color,
        "line_width": selected_line_width,
        "marker_style": selected_marker_style,
        "title": custom_title,
        "size": plot_size
    })

# Button to clear all plots
if st.sidebar.button("\U0001F5D1 Clear All Plots"):
    st.session_state.active_plots = []

# Drag-and-drop sorting of plots
if st.session_state.active_plots:
    st.session_state.active_plots = sort_items(st.session_state.active_plots, "Drag to rearrange plots:")

# Generate and display plots in a flexible grid layout
st.subheader("\U0001F4C8 Live 5G Measurements")
data = generate_data()
marker_dict = {"circle": "circle", "square": "square", "diamond": "diamond", "cross": "x"}

for plot in st.session_state.active_plots:
    meas, plot_type, color, line_width, marker_style, title, size = (
        plot["measurement"], plot["plot_type"], plot["color"], 
        plot["line_width"], plot["marker_style"], plot["title"], plot["size"]
    )
    
    fig = go.Figure()
    if plot_type == "Line Chart":
        y_values = np.random.uniform(0, 100, 10)  # Simulating 10 time samples
        fig.add_trace(go.Scatter(y=y_values, x=list(range(10)), mode='lines', name=meas, line=dict(color=color, width=line_width)))
        fig.update_layout(title=title, xaxis_title="Time", yaxis_title="Value")
    elif plot_type == "Gauge":
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=data[meas],
            title={"text": title},
            gauge={"axis": {"range": [0, 100] if meas != "BLER" else [0, 1]}, "bar": {"color": color}}
        ))
    elif plot_type == "Scatter (for Constellation)" and meas == "Constellation":
        fig.add_trace(go.Scatter(
            x=data["Constellation"][:, 0], 
            y=data["Constellation"][:, 1], 
            mode='markers', 
            marker=dict(color=color, symbol=marker_dict[marker_style])
        ))
        fig.update_layout(title=title, xaxis_title="I", yaxis_title="Q")
    
    st.plotly_chart(fig, use_container_width=False, height=size)

# Auto-refresh every few seconds
st.sidebar.write("\U0001F504 The data updates automatically every time you refresh.")
