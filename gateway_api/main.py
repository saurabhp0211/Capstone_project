from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from orchestrator.graph import app_workflow

app = FastAPI(title="Loan Approval Agentic API")

# Define exactly what data the API expects
class LoanApplication(BaseModel):
    applicant_id: str
    age: int
    income: float
    employment_type: str
    credit_score: int
    loan_amount: float
    tenure: int            
    location: str          
    existing_liabilities: float

@app.post("/api/v1/loan/apply")
async def process_loan(application: LoanApplication):
    try:
        # Convert Pydantic model to dict and start the LangGraph workflow
        initial_state = application.dict()
        
        # Invoke the graph
        result = app_workflow.invoke(initial_state)
        
        # Return the final decision
        return {
            "status": "success",
            "applicant_id": result["applicant_id"],
            "decision": result["final_decision"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

