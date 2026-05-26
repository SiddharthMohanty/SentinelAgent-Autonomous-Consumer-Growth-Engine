import json
import os
from langchain_core.tools import tool

# Dynamically calculate the path to data/customers.json so it runs anywhere
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(BASE_DIR, "data", "customers.json")

@tool
def fetch_customer_data(customer_id: str) -> dict:
    """
    Fetches customer CRM data based on the provided customer ID.
    Returns a dictionary containing LTV, tier, tenure, and recent tickets.
    """
    try:
        with open(DATA_PATH, "r") as f:
            data = json.load(f)
        
        if customer_id in data:
            return data[customer_id]
        else:
            return {"error": f"Customer ID {customer_id} not found in Database."}
            
    except FileNotFoundError:
        return {"error": "Database file not found. Ensure customers.json exists."}