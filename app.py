import streamlit as st
import json
import os
import time
from core.workflow import build_graph

st.set_page_config(page_title="SentinelAgent: Autonomous Churn Engine", layout="wide")
st.title("🛡️ SentinelAgent POC")
st.markdown("Autonomous workflow for real-time churn mitigation and retention.")

# Load mock data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "customers.json")

with open(DATA_PATH, "r") as f:
    customers = json.load(f)

# --- STATE INITIALIZATION ---
if "graph_running" not in st.session_state:
    st.session_state.graph_running = False
if "run_timestamp" not in st.session_state:
    st.session_state.run_timestamp = str(int(time.time()))

# Sidebar Setup
st.sidebar.header("Simulation Settings")
selected_cust_id = st.sidebar.selectbox(
    "Select Customer Profile:", 
    options=list(customers.keys()),
    format_func=lambda x: f"{x} - {customers[x]['name']}"
)
st.sidebar.json(customers[selected_cust_id])

trigger_event = st.sidebar.text_area(
    "Incoming Trigger Event (Support Ticket/Chat):",
    value="Our dashboard is completely down and we are losing money. Fix this now or we cancel."
)

@st.cache_resource
def get_graph():
    return build_graph()

graph = get_graph()

# --- FIXED: Dynamic Thread ID prevents checkpoint collisions ---
config = {
    "configurable": {
        "thread_id": f"thread_{selected_cust_id}_{st.session_state.run_timestamp}"
    }
}

# Primary trigger button
if st.sidebar.button("Run Autonomous Agent"):
    # Generate a fresh timestamp to force a brand-new LangGraph timeline
    st.session_state.run_timestamp = str(int(time.time()))
    st.session_state.graph_running = True
    
    # Re-verify config with the brand new timestamp
    config = {
        "configurable": {
            "thread_id": f"thread_{selected_cust_id}_{st.session_state.run_timestamp}"
        }
    }
    
    initial_state = {
        "customer_id": selected_cust_id,
        "trigger_event": trigger_event,
        "messages": []
    }
    
    # Consume the stream to move the graph forward up to the interrupt gate
    with st.spinner("Agents are reasoning..."):
        for event in graph.stream(initial_state, config=config):
            pass 

# --- RENDERING ENGINE: Reads directly from LangGraph Database ---
if st.session_state.graph_running:
    # Pull the true, absolute state directly out of LangGraph's memory saver
    current_graph_state = graph.get_state(config)
    vals = current_graph_state.values  # This is our source of truth dict
    
    if vals:
        st.subheader("Agent Execution Trace")
        
        if "customer_data" in vals:
            with st.expander("✅ Node Executed: PROFILER", expanded=True):
                st.write("**Action:** Fetched CRM Data")
                st.json(vals["customer_data"])
                
        if "churn_risk_score" in vals:
            with st.expander("✅ Node Executed: ASSESSOR", expanded=True):
                st.write(f"**Calculated Risk:** `{vals['churn_risk_score']}`")
                st.write(f"**LLM Reasoning:** {vals['reasoning']}")
                
        if "recommended_action" in vals:
            with st.expander("✅ Node Executed: PROPOSER (Rules Engine)", expanded=True):
                st.write(f"**Calculated Strategy Option:** `{vals['recommended_action']}`")
                st.write(f"**Requires Human Overlook Gate:** `{vals['requires_approval']}`")

        # Handle Human Decision Gate
        if current_graph_state.next:
            st.error("🚨 CRITICAL CHURN RISK DETECTED: Execution Paused.")
            st.warning("The system has computed a mitigation strategy option but requires human authorization to commit.")
            
            # FIXED: Guaranteed to display the calculated action string now
            st.info(f"👉 **Proposed Action for Review:** {vals.get('recommended_action')}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👍 Approve & Execute"):
                    st.success("Action Approved. Committing agent thread...")
                    
                    # Resume execution through the final gate node
                    for event in graph.stream(None, config=config):
                        pass
                        
                    st.rerun()  # Refresh layout to show final success state
            with col2:
                if st.button("👎 Reject & Route to Human"):
                    st.error("Action Rejected. Escalated to account manager.")
        else:
            # Final success screen display
            st.balloons()
            st.success("🎉 Workflow completed successfully!")
            st.markdown("### 🚀 Final Desired Strategy Dispatched")
            st.info(f"**Executed Strategy:** {vals.get('recommended_action', 'Standard automated processing.')}")