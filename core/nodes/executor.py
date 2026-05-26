from core.state import GraphState

def run_executor(state: GraphState) -> dict:
    """
    Determines the specific retention action based on the LLM's risk assessment 
    and the hard CRM data (LTV, Tier).
    """
    risk = state.get("churn_risk_score")
    data = state.get("customer_data", {})
    
    ltv = data.get("ltv", 0)
    tier = data.get("tier", "Starter")
    
    action = "No action defined."
    requires_approval = False
    
    # Business Logic Rules Engine
    if risk == "High":
        if ltv > 10000 or tier == "Enterprise":
            action = "Drafted High-Value Retention Package (Custom Discount & Account Manager Escalation)"
            requires_approval = True  # Triggers the HITL gate
        else:
            action = "Auto-emailed standard 20% retention discount link."
            
    elif risk == "Medium":
        action = "Flagged in support queue for priority response within 2 hours."
        
    else:
        action = "Standard processing. No immediate retention action required."
        
    return {
        "recommended_action": action,
        "requires_approval": requires_approval
    }