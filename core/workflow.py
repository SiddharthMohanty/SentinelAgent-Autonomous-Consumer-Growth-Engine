from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from core.state import GraphState
from core.nodes.profiler import run_profiler
from core.nodes.assessor import run_assessor
from core.nodes.executor import run_executor

# We create a dummy node to represent the final "Commit to Database / Send API" action
def commit_action(state: GraphState) -> dict:
    return {}

def build_graph():
    workflow = StateGraph(GraphState)
    
    # 1. Register the nodes
    workflow.add_node("profiler", run_profiler)
    workflow.add_node("assessor", run_assessor)
    workflow.add_node("proposer", run_executor)  # Runs the logic and updates the state
    workflow.add_node("executor", commit_action) # The final gate where the graph will pause
    
    # 2. Define the flow
    workflow.add_edge(START, "profiler")
    workflow.add_edge("profiler", "assessor")
    
    def route_based_on_risk(state: GraphState):
        if state.get("churn_risk_score") == "Low":
            return "end"
        return "proposer"
        
    workflow.add_conditional_edges(
        "assessor", 
        route_based_on_risk,
        {"proposer": "proposer", "end": END}
    )
    
    # The proposer hands off to the executor
    workflow.add_edge("proposer", "executor")
    workflow.add_edge("executor", END)
    
    memory = MemorySaver()
    
    # 3. We interrupt right BEFORE the final commit, meaning the proposer has already run!
    app = workflow.compile(
        checkpointer=memory,
        interrupt_before=["executor"]
    )
    
    return app