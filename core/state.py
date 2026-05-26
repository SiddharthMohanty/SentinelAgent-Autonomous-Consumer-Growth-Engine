from typing import TypedDict, Annotated, Sequence, Any
from operator import add
from langchain_core.messages import BaseMessage

class GraphState(TypedDict):
    """
    Represents the state of our multi-agent workflow.
    Every node in the graph will read and update this dictionary.
    """
    customer_id: str
    trigger_event: str
    
    # Data populated by the Profiler Agent
    customer_data: dict[str, Any]
    
    # Data populated by the Risk Assessor Agent
    churn_risk_score: str  # e.g., "Low", "Medium", "High"
    reasoning: str
    
    # Data populated by the Action Executor Agent
    recommended_action: str
    requires_approval: bool
    
    # The reducer 'add' ensures messages are appended, not overwritten
    messages: Annotated[Sequence[BaseMessage], add]