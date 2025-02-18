import streamlit as st
import plotly.graph_objects as go
import numpy as np
from streamlit_sortables import sort_items

# Load Google Fonts dynamically
GOOGLE_FONTS = [
    "Roboto", "Open Sans", "Montserrat", "Lato", "Poppins", "Raleway", "Merriweather",
    "Oswald", "Nunito", "Playfair Display", "Quicksand", "Ubuntu", "Pacifico", "Caveat"
]

# Simulated 5G measurement data
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
plot_types = ["Line Chart", "Gauge", "Scatter (for Constellation)", "Bar Chart"]

# Session state to store active plots
if "active_plots" not in st.session_state:
    st.session_state.active_plots = []

# Select measurement, plot type, and styling
selected_measurement = st.sidebar.selectbox("Select Measurement", measurements)
selected_plot_type = st.sidebar.selectbox("Select Plot Type", plot_types)
selected_color = st.sidebar.color_picker("Select Plot Color", "#1f77b4")
selected_line_width = st.sidebar.slider("Line Thickness", 1, 5, 2)
selected_marker_style = st.sidebar.selectbox("Marker Style", ["circle", "square", "diamond", "cross"])
plot_width = st.sidebar.slider("Plot Width (%)", 20, 100, 50)
plot_height = st.sidebar.slider("Plot Height (px)", 200, 800, 400)

# Button to add plot
if st.sidebar.button("➕ Add Plot"):
    st.session_state.active_plots.append({
        "measurement": selected_measurement,
        "plot_type": selected_plot_type,
        "color": selected_color,
        "line_width": selected_line_width,
        "marker_style": selected_marker_style,
        "width": plot_width,
        "height": plot_height
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

# Generate and display plots
st.subheader("📈 Live 5G Measurements")
data = generate_data()
marker_dict = {"circle": "circle", "square": "square", "diamond": "diamond", "cross": "x"}

if st.session_state.active_plots:
    for plot in st.session_state.active_plots:
        meas, plot_type, color, line_width, marker_style, width, height = (
            plot["measurement"], plot["plot_type"], plot["color"],
            plot["line_width"], plot["marker_style"], plot["width"], plot["height"]
        )

        # Container with resizable width & height
        with st.container():
            st.markdown(
                f'<div style="width:{width}%; height:{height}px;">', 
                unsafe_allow_html=True
            )

            if plot_type == "Line Chart":
                y_values = np.random.uniform(0, 100, 10)  # Simulated 10 time samples
                fig = go.Figure(go.Scatter(y=y_values, x=list(range(10)), mode='lines', name=meas, 
                                           line=dict(color=color, width=line_width)))
                fig.update_layout(title=f"{meas} - Line Chart", xaxis_title="Time", yaxis_title="Value")
                st.plotly_chart(fig, use_container_width=True)

            elif plot_type == "Gauge":
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=data[meas],
                    title={"text": meas},
                    gauge={"axis": {"range": [0, 100] if meas != "BLER" else [0, 1]}, "bar": {"color": color}}
                ))
                st.plotly_chart(fig, use_container_width=True)

            elif plot_type == "Scatter (for Constellation)" and meas == "Constellation":
                fig = go.Figure(go.Scatter(
                    x=data["Constellation"][:, 0], y=data["Constellation"][:, 1],
                    mode='markers', marker=dict(color=color, symbol=marker_dict[marker_style])
                ))
                fig.update_layout(title="Constellation Plot", xaxis_title="I", yaxis_title="Q")
                st.plotly_chart(fig, use_container_width=True)

            # Close resizable div
            st.markdown("</div>", unsafe_allow_html=True)

# Auto-refresh info
st.sidebar.write("🔄 The data updates automatically every time you refresh.")
