import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from streamlit_sortables import sort_items

# Simulated 5G measurement data (replace with real data)
def generate_data():
    return {
        "MCS": np.random.randint(0, 28),
        "SINR": np.random.uniform(-10, 30),
        "Throughput": np.random.uniform(10, 100),
        "BLER": np.random.uniform(0, 1),
        "Constellation": np.random.uniform(-1, 1, (100, 2))  # 100 sample points
    }

# UI Layout
st.title("📡 5G RAN Network Dashboard")
st.sidebar.header("📊 Manage Your Dashboard")

# Available measurement options
measurements = ["MCS", "SINR", "Throughput", "BLER", "Constellation"]
plot_types = ["Line Chart", "Gauge", "Scatter (for Constellation)"]

# Session state to store active plots
if "active_plots" not in st.session_state:
    st.session_state.active_plots = []

# Select measurement & plot type
selected_measurement = st.sidebar.selectbox("Select Measurement", measurements)
selected_plot_type = st.sidebar.selectbox("Select Plot Type", plot_types)

# Button to add plot
if st.sidebar.button("➕ Add Plot"):
    st.session_state.active_plots.append({"measurement": selected_measurement, "plot_type": selected_plot_type})

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

# Generate and display plots
st.subheader("📈 Live 5G Measurements")
data = generate_data()

for plot in st.session_state.active_plots:
    meas, plot_type = plot["measurement"], plot["plot_type"]

    if plot_type == "Line Chart":
        y_values = np.random.uniform(0, 100, 10)  # Simulating 10 time samples
        fig = go.Figure(go.Scatter(y=y_values, x=list(range(10)), mode='lines', name=meas))
        fig.update_layout(title=f"{meas} - Line Chart", xaxis_title="Time", yaxis_title="Value")
        st.plotly_chart(fig)

    elif plot_type == "Gauge":
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=data[meas],
            title={"text": meas},
            gauge={"axis": {"range": [0, 100] if meas != "BLER" else [0, 1]}}
        ))
        st.plotly_chart(fig)

    elif plot_type == "Scatter (for Constellation)" and meas == "Constellation":
        fig = go.Figure(go.Scatter(x=data["Constellation"][:, 0], y=data["Constellation"][:, 1], mode='markers'))
        fig.update_layout(title="Constellation Plot", xaxis_title="I", yaxis_title="Q")
        st.plotly_chart(fig)

# Auto-refresh every few seconds
st.sidebar.write("🔄 The data updates automatically every time you refresh.")