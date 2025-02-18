import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Simulated 5G measurement data (replace with real-time data source)
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
st.sidebar.header("📊 Select Measurements & Plot Type")

# Measurement selection
measurements = ["MCS", "SINR", "Throughput", "BLER", "Constellation"]
selected_measurements = st.sidebar.multiselect("Select Measurements", measurements, default=["MCS", "SINR"])

# Plot type selection
plot_types = ["Line Chart", "Gauge", "Scatter (for Constellation)"]
selected_plot_type = st.sidebar.selectbox("Select Plot Type", plot_types)

# Generate data
data = generate_data()

# Plotting logic
st.subheader("📈 Live 5G Measurements")

if selected_plot_type == "Line Chart":
    fig = go.Figure()
    for meas in selected_measurements:
        if meas != "Constellation":
            y_values = np.random.uniform(0, 100, 10)  # Simulating 10 time samples
            fig.add_trace(go.Scatter(y=y_values, x=list(range(10)), mode='lines', name=meas))
    fig.update_layout(title="Line Chart of Selected Measurements", xaxis_title="Time", yaxis_title="Value")
    st.plotly_chart(fig)

elif selected_plot_type == "Gauge":
    for meas in selected_measurements:
        if meas in ["MCS", "SINR", "Throughput", "BLER"]:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=data[meas],
                title={"text": meas},
                gauge={"axis": {"range": [0, 100] if meas != "BLER" else [0, 1]}}
            ))
            st.plotly_chart(fig)

elif selected_plot_type == "Scatter (for Constellation)":
    if "Constellation" in selected_measurements:
        fig = go.Figure(go.Scatter(x=data["Constellation"][:, 0], y=data["Constellation"][:, 1], mode='markers'))
        fig.update_layout(title="Constellation Plot", xaxis_title="I", yaxis_title="Q")
        st.plotly_chart(fig)
    else:
        st.warning("Please select 'Constellation' to view this plot.")

# Auto-refresh every few seconds
st.sidebar.write("🔄 The data updates automatically every time you refresh.")
