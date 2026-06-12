from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ApplicantDB")

@mcp.tool()
def evaluate_applicant(age: int, income: float, employment_type: str) -> dict:
    """Evaluates an applicant's profile to determine stability and risk."""
    
    # Mock logic for evaluation
    stability_score = min(100, int((income / 1000) + (age * 0.5)))
    emp_risk = "Low" if employment_type.lower() in ["salaried", "full-time"] else "High"
    
    return {
        "income_stability_score": stability_score,
        "employment_risk": emp_risk,
        "credit_history_summary": "No major defaults found.",
        "application_completeness_flags": ["Valid Age", "Valid Income", "Employment Verified"]
    }