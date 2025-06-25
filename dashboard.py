import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

LOG_FILE = "usage_log.csv"
CONFIG_FILE = "focus_config.json"

def load_focus_config():
    if not os.path.exists(CONFIG_FILE):
        return {"focus_mode": False, "time_limits": {}}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_focus_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

st.set_page_config(layout="wide")
st.title("💻 Digital Wellbeing")

if not os.path.exists(LOG_FILE):
    st.warning("No usage data yet. Run tracker.py first.")
    st.stop()

df = pd.read_csv(LOG_FILE, names=["timestamp", "app", "category", "duration"])
df["timestamp"] = pd.to_datetime(df["timestamp"])

config = load_focus_config()
focus_on = st.toggle("🔒 Focus Mode", value=config["focus_mode"])
config["focus_mode"] = focus_on
save_focus_config(config)

st.header("📊 App Usage")
app_usage = df.groupby("app")["duration"].sum().reset_index()
st.bar_chart(app_usage.set_index("app"))

category_totals = df.groupby("category")["duration"].sum().reset_index()
fig_pie = px.pie(category_totals, values="duration", names="category", title="Time by Category")
st.plotly_chart(fig_pie)

productive = df[df["category"] == "Productive"]["duration"].sum()
total = df["duration"].sum()
focus_score = (productive / total) * 100 if total else 0
st.metric("🎯 Focus Score", f"{focus_score:.2f} %")

for app, limit in config["time_limits"].items():
    used = df[df["app"] == app]["duration"].sum()
    if used >= 0.8 * limit:
        st.warning(f"⚠️ {app} close to limit: {used:.0f}s / {limit}s")
