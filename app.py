
import streamlit as st
import pandas as pd
import joblib
ai = joblib.load('green_allocator_ai.pkl')
df = pd.read_csv('cloud_data.csv')

def green_allocate(cpu, mem, io, region):
    carbon = {'EU-Green':250, 'US-Coal':650, 'Asia-Mix':480}[region]
    renewable = 1 if region=='EU-Green' else 0
    energy = ai.predict([[cpu, mem, io, carbon, renewable]])[0]
    score = max(0, min(1, 1 - energy/350 + renewable*0.15))
    action = "RUN" if score>0.58 else "MIGRATE to EU-Green"
    return f"**{energy:.0f} Wh** → **{action}** | Sustainability: {score:.2f}"

st.set_page_config("Green Cloud", layout="wide")
st.title("Sustainable Cloud Allocator")
c1, c2 = st.columns([1,1])

with c1:
    st.subheader("Live Workload Optimizer")
    cpu = st.slider("CPU %", 0.0, 1.0, 0.75, 0.05)
    mem = st.slider("RAM %", 0.0, 1.0, 0.60, 0.05)
    io  = st.slider("Disk IO (MB/s)", 0, 800, 300, 50)
    region = st.selectbox("Data Center", ["EU-Green", "US-Coal", "Asia-Mix"])
    if st.button("ALLOCATE NOW", type="primary"):
        st.success(green_allocate(cpu, mem, io, region))

with c2:
    st.subheader("Auto-Shutdown List")
    idle = df[df['cpu_usage']<0.1]['vm_id'].unique()
    savings = len(idle)*42
    st.metric("Idle VMs", len(idle), f"Save {savings} Wh")
    st.bar_chart(df['sustainability_score'].round(2).value_counts().sort_index())

st.download_button("Export Full Report", df.to_csv(), "green_report.csv")
