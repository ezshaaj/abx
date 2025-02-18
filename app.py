import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Load Google Fonts
GOOGLE_FONTS = [
    "Roboto", "Open Sans", "Montserrat", "Lato", "Poppins", "Raleway", 
    "Merriweather", "Oswald", "Nunito", "Playfair Display", "Quicksand", 
    "Ubuntu", "Pacifico", "Caveat"
]

# Generate simulated 5G measurement data
def generate_data():
    return {
        "MCS": np.random.randint(0, 28),
        "SINR": np.random.uniform(-10, 30),
        "Throughput": np.random.uniform(10, 100),
        "BLER": np.random.uniform(0, 1),
        "Constellation": np.random.uniform(-1, 1, (100, 2))  # 100 sample points for scatter
    }

# UI Layout
st.set_page_config(page_title="5G RAN Dashboard", layout="wide")
st.title("📡 5G RAN Network Dashboard")
st.sidebar.header("🎨 Customize Your Dashboard")

# Custom Theme Settings
selected_font = st.sidebar.selectbox("Select Font", GOOGLE_FONTS)
selected_measurement = st.sidebar.selectbox("Select Measurement", ["MCS", "SINR", "Throughput", "BLER", "Constellation"])
selected_plot_type = st.sidebar.selectbox("Select Plot Type", ["Gauge", "Line Chart", "Scatter", "Bar Chart"])
selected_color = st.sidebar.color_picker("Select Plot Color", "#1f77b4")
selected_line_width = st.sidebar.slider("Line Thickness", 1, 5, 2)
selected_width = st.sidebar.slider("Plot Width (px)", 200, 800, 400)
selected_height = st.sidebar.slider("Plot Height (px)", 200, 800, 400)
custom_title = st.sidebar.text_input("Enter Custom Plot Title", "My Custom Plot")

# Session state for active plots
if "active_plots" not in st.session_state:
    st.session_state.active_plots = {}

# Add new plot
if st.sidebar.button("➕ Add Plot"):
    plot_id = str(np.random.randint(1000, 9999))  # Unique ID
    st.session_state.active_plots[plot_id] = {
        "measurement": selected_measurement,
        "plot_type": selected_plot_type,
        "color": selected_color,
        "line_width": selected_line_width,
        "width": selected_width,
        "height": selected_height,
        "title": custom_title
    }

# Clear all plots
if st.sidebar.button("🗑 Clear All Plots"):
    st.session_state.active_plots = {}

# Generate plots
st.subheader("📈 Live 5G Measurements")
data = generate_data()
plots_to_delete = []

if st.session_state.active_plots:
    for plot_id, plot in list(st.session_state.active_plots.items()):
        meas, plot_type, color, line_width, width, height, title = (
            plot["measurement"], plot["plot_type"], plot["color"], plot["line_width"],
            plot["width"], plot["height"], plot["title"]
        )

        # Create Plot
        fig = go.Figure()

        if plot_type == "Line Chart":
            y_values = np.random.uniform(0, 100, 10)
            fig.add_trace(go.Scatter(y=y_values, x=list(range(10)), mode='lines',
                                     line=dict(color=color, width=line_width)))
            fig.update_layout(title=title, width=width, height=height)

        elif plot_type == "Gauge":
            fig.add_trace(go.Indicator(
                mode="gauge+number",
                value=data[meas],
                title={"text": title},
                gauge={"axis": {"range": [0, 100] if meas != "BLER" else [0, 1]}, "bar": {"color": color}}
            ))
            fig.update_layout(width=width, height=height)

        elif plot_type == "Scatter" and meas == "Constellation":
            fig.add_trace(go.Scatter(
                x=data["Constellation"][:, 0], y=data["Constellation"][:, 1],
                mode='markers', marker=dict(color=color)
            ))
            fig.update_layout(title=title, width=width, height=height)

        elif plot_type == "Bar Chart":
            values = np.random.uniform(10, 100, 5)
            labels = ["A", "B", "C", "D", "E"]
            fig.add_trace(go.Bar(x=labels, y=values, marker_color=color))
            fig.update_layout(title=title, width=width, height=height)

        # Display plot with a delete button on top-right
        col1, col2 = st.columns([9, 1])
        with col1:
            st.plotly_chart(fig, config={"displayModeBar": True})
        with col2:
            if st.button("❌", key=f"remove_{plot_id}"):
                plots_to_delete.append(plot_id)

# Remove selected plots
for plot_id in plots_to_delete:
    del st.session_state.active_plots[plot_id]
