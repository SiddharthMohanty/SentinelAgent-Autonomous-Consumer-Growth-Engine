import os
from typing import Literal
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from core.state import GraphState

# Load environment variables (API keys)
load_dotenv()

# 1. Define the exact JSON structure we require from the LLM
class ChurnAssessment(BaseModel):
    risk_level: Literal["Low", "Medium", "High"] = Field(
        description="The calculated churn risk level based on the customer context."
    )
    reasoning: str = Field(
        description="A brief, 1-2 sentence explanation of why this risk level was chosen."
    )

def run_assessor(state: GraphState) -> dict:
    """
    Analyzes unstructured text (the trigger event) and CRM data (the profile) 
    to assess churn risk and output a structured schema.
    """
    # Initialize the LLM with a temperature of 0 for highly deterministic reasoning
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    # Bind the Pydantic schema to the LLM to force structured JSON output
    structured_llm = llm.with_structured_output(ChurnAssessment)

    # 2. Design the System Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert Autonomous Customer Success Agent. 
        Your job is to evaluate the churn risk of a customer based on their historical profile and their latest support ticket/event.
        
        Rules:
        - Consider their LTV (Lifetime Value), Tier, and past tickets.
        - If they use explicit churn language ("cancel", "competitor", "leaving"), risk is HIGH.
        - If there is a severe technical/security block for an Enterprise client, risk is HIGH.
        - If it is a simple user error (password reset) or a low LTV client with a minor issue, risk is LOW.
        - If they are frustrated but the issue is manageable, risk is MEDIUM.
        """),
        ("user", "Customer Profile Data:\n{customer_data}\n\nLatest Trigger Event:\n{trigger_event}")
    ])

    # 3. Chain the prompt and the LLM (LCEL)
    chain = prompt | structured_llm
    
    # 4. Execute the reasoning engine using the current graph state
    result = chain.invoke({
        "customer_data": state.get("customer_data"),
        "trigger_event": state.get("trigger_event")
    })

    # Return the dictionary to update the graph state
    return {
        "churn_risk_score": result.risk_level,
        "reasoning": result.reasoning
    }