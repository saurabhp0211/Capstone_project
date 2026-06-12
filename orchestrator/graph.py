import os
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

# Define the state that gets passed between nodes
class LoanState(TypedDict):
    applicant_id: str
    age: int
    income: float
    employment_type: str
    credit_score: int
    loan_amount: float
    tenure: int            
    location: str
    existing_liabilities: float
    
    # Outputs gathered along the way
    stability_data: dict
    risk_data: dict
    final_decision: dict

# Initialize Claude
llm = ChatAnthropic(
    model="global.anthropic.claude-sonnet-4-6",
    temperature=0,
    base_url="https://llmgw-wp.tekstac.com"
)

# nodes

def assess_applicant(state: LoanState):
    """Node 1: Simulates calling the ApplicantDB MCP Server"""
    # In a full production MCP setup, you would use mcp.client here.
    # For this assignment, we replicate the tool's expected output format based on state.
    stability_score = min(100, int((state["income"] / 1000) + (state["age"] * 0.5)))
    return {"stability_data": {"stability_score": stability_score}}

def evaluate_risk(state: LoanState):
    """Node 2: Simulates calling the RiskRulesDB MCP Server"""
    dti = state["existing_liabilities"] / state["income"] if state["income"] > 0 else 1.0
    risk_level = "Low" if state["credit_score"] >= 750 else "High"
    return {"risk_data": {"dti": dti, "credit_risk": risk_level}}

def synthesize_decision(state: LoanState):
    """Node 3: Uses Claude to make the final decision based on gathered data"""
    prompt = f"""
    Analyze this loan application and classify as Approved, Rejected, or Requires Manual Review.
    Data:
    - Income: {state['income']}, Loan Amount: {state['loan_amount']}
    - DTI: {state['risk_data']['dti']:.2f}, Credit Risk: {state['risk_data']['credit_risk']}
    - Stability Score: {state['stability_data']['stability_score']}
    
    Respond strictly in JSON format with keys: "Classification", "Risk Score", "Explanation".
    Do NOT wrap the response in markdown blocks like ```json. Output raw JSON only.
    """
    
    response = llm.invoke(prompt)
    content = response.content.strip()
    
    # Strip markdown formatting if Claude still includes it
    if content.startswith("```json"):
        content = content.replace("```json", "").replace("```", "").strip()
    elif content.startswith("```"):
        content = content.replace("```", "").strip()
        
    import json
    try:
        decision = json.loads(content)
    except Exception as e:
        # If it still fails, print the actual error to the UI so we can debug it
        decision = {"Classification": "Review", "Risk Score": 50, "Explanation": f"JSON Parse Error. Raw Output: {content}"}
        
    return {"final_decision": decision}



# --- Build the Graph ---
workflow = StateGraph(LoanState)

workflow.add_node("applicant_agent", assess_applicant)
workflow.add_node("risk_agent", evaluate_risk)
workflow.add_node("decision_agent", synthesize_decision)

workflow.set_entry_point("applicant_agent")
workflow.add_edge("applicant_agent", "risk_agent")
workflow.add_edge("risk_agent", "decision_agent")
workflow.add_edge("decision_agent", END)

# Compile it!
app_workflow = workflow.compile()