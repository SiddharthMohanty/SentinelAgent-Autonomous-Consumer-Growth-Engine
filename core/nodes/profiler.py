from core.state import GraphState
from core.tools.db_tools import fetch_customer_data

def run_profiler(state: GraphState) -> dict:
    """
    Fetches CRM data using the db_tools and adds it to the graph state.
    """
    customer_id = state.get("customer_id")
    
    # Invoke the tool synchronously
    data = fetch_customer_data.invoke({"customer_id": customer_id})
    
    # Return a dictionary containing ONLY the keys you want to update in the state
    return {"customer_data": data}