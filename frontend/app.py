import os
import requests
import pandas as pd
import streamlit as st

API_URL = os.getenv("API_URL", "http://backend:8000")

st.set_page_config(
    page_title="CloudOps Monitor",
    layout="wide"
)

st.title("CloudOps Monitor Dashboard")

col1, col2, col3 = st.columns(3)

try:
    response = requests.get(f"{API_URL}/servers")
    servers = response.json() if response.status_code == 200 else []
except Exception:
    servers = []

total = len(servers)
healthy = len([s for s in servers if s["status"] == "healthy"])
unhealthy = len([s for s in servers if s["status"] == "unhealthy"])

col1.metric("Total Servers", total)
col2.metric("Healthy Servers", healthy)
col3.metric("Unhealthy Servers", unhealthy)

st.divider()

st.subheader("Add Server")

with st.form("server_form"):
    name = st.text_input("Server Name")
    ip = st.text_input("IP Address")
    environment = st.selectbox("Environment", ["dev", "staging", "production"])
    region = st.text_input("Region", "ap-south-1")
    owner = st.text_input("Owner")
    application = st.text_input("Application Name")

    submitted = st.form_submit_button("Add Server")

    if submitted:
        payload = {
            "name": name,
            "ip": ip,
            "environment": environment,
            "region": region,
            "owner": owner,
            "application": application
        }

        res = requests.post(f"{API_URL}/servers", json=payload)

        if res.status_code == 200:
            st.success("Server added successfully")
            st.rerun()
        else:
            st.error("Failed to add server")

st.divider()

st.subheader("Server Inventory")

if servers:
    df = pd.DataFrame(servers)
    st.dataframe(df, use_container_width=True)

    st.subheader("Update Server Status")

    server_ids = [s["id"] for s in servers]
    selected_id = st.selectbox("Select Server ID", server_ids)
    status = st.selectbox("Status", ["healthy", "unhealthy"])

    if st.button("Update Status"):
        res = requests.patch(
            f"{API_URL}/servers/{selected_id}/status",
            params={"status": status}
        )

        if res.status_code == 200:
            st.success("Status updated")
            st.rerun()
        else:
            st.error("Failed to update status")
else:
    st.info("No servers added yet")

st.divider()

st.subheader("Backend Health")

try:
    health = requests.get(f"{API_URL}/health").json()
    st.json(health)
except Exception as e:
    st.error(f"Backend not reachable: {e}")
