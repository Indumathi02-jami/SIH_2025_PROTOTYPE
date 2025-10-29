import streamlit as st
from streamlit_folium import st_folium
import folium
import time
import random

# --- Streamlit Page Config ---
st.set_page_config(
    page_title="College Bus Tracker",
    page_icon="🚌",
    layout="wide",
)

# --- App Header ---
st.title("🚌 College Bus Tracking System")
st.markdown("#### Powered by Bluetooth Switch System (No GPS)")
st.markdown("---")

# --- Simulated Bus Data (in real system, fetched from Bluetooth-based events) ---
buses = [
    {"number": "CBE-101", "halt": "Main Block", "location": [18.0868, 83.4017], "status": "En Route"},
    {"number": "CBE-102", "halt": "Main Gate", "location": [18.0872, 83.4010], "status": "At Halt"},
    {"number": "CBE-103", "halt": "Hostel Gate", "location": [18.0859, 83.4022], "status": "Departed"},
]


# --- Layout: Sidebar for Controls ---
st.sidebar.header("🔧 Control Panel")
refresh = st.sidebar.button("🔄 Refresh Bus Status")

# --- Simulate Random Status Change ---
if refresh:
    for bus in buses:
        bus["status"] = random.choice(["At Halt", "Departed", "En Route"])
        bus["halt"] = random.choice(["Science Block", "Main Gate", "Canteen", "Hostel", "Library"])
        # Small random offset for location movement
        bus["location"][0] += random.uniform(-0.0005, 0.0005)
        bus["location"][1] += random.uniform(-0.0005, 0.0005)
    st.success("Bus statuses updated!")

# --- Folium Map ---
lendi_location = [18.1060, 83.3950]  # Center of the campus
m = folium.Map(location=lendi_location, zoom_start=16)

for bus in buses:
    color = {
        "At Halt": "blue",
        "Departed": "red",
        "En Route": "green"
    }.get(bus["status"], "gray")

    folium.Marker(
        location=bus["location"],
        popup=f"<b>Bus:</b> {bus['number']}<br><b>Halt:</b> {bus['halt']}<br><b>Status:</b> {bus['status']}",
        tooltip=f"{bus['number']} - {bus['status']}",
        icon=folium.Icon(color=color, icon="bus", prefix="fa"),
    ).add_to(m)

# --- Display Map ---
st_folium(m, width=1100, height=550)

# --- Bus Status Table ---
st.markdown("### 📋 Current Bus Status")
st.dataframe(
    [{"Bus No": b["number"], "Current Halt": b["halt"], "Status": b["status"]} for b in buses],
    use_container_width=True
)

# --- Footer ---
st.markdown("---")
st.markdown("<p style='text-align:center; color:gray;'>© 2025 College Bus Tracker | Built with Streamlit & Folium</p>", unsafe_allow_html=True)
