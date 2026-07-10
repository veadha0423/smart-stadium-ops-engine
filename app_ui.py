import streamlit as st
import requests

st.set_page_config(page_title="Stadium Ops Engine", page_icon="🏟️", layout="wide")

game_day = random.randint(1, 100)
st.title("🏟️ Smart Stadium & Tournament Operations Engine")
st.subheader(f"Game Day {game_day}: Production Triage Dashboard")

uploaded_file = st.file_uploader("Upload Unstructured Match-Day PDF Log", type=["pdf"])
BACKEND_URL = "https://smart-stadium-ops-engine.onrender.com"

if uploaded_file is not None:
    if st.button("Execute Tactical Triage Run"):
        with st.spinner("Processing logs and querying intelligence matrix..."):
            # We connect this to your backend deployment URL later
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            try:
                response = requests.post(f"{BACKEND_URL}/api/v1/incident-triage", files=files)
                if response.status_code == 200:
                    data = response.json()
                    
                    # Layout Metrics
                    col1, col2 = st.columns(2)
                    col1.metric("Primary Threat Sector", data["primary_threat_sector"].upper())
                    col2.metric("Highest Severity Score", f"{data['highest_severity_score']}/100")
                    
                    st.error(f"🚨 **AI Operational Directive:**\n{data['ai_dispatch_directive']}")
                    
                    st.write("### 📊 Departmental Severity Matrix")
                    st.json(data["severity_matrix"])
                else:
                    st.error("Backend Server Error.")
            except Exception as e:
                st.error(f"Connection Failed: {e}")