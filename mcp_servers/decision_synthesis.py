from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DecisionSynthesis")

@mcp.tool()
def synthesize_decision(stability_score: int, dti: float, credit_risk: str) -> dict:
    """Provides a baseline decision synthesis based on risk factors."""
    
    if credit_risk == "High" or dti > 0.5:
        classification = "Reject"
        confidence = 0.85
    elif credit_risk == "Low" and dti < 0.3:
        classification = "Approve"
        confidence = 0.90
    else:
        classification = "Review"
        confidence = 0.60
        
    return {
        "classification": classification,
        "risk_score": max(0, 100 - int(dti * 100)),
        "confidence_level": confidence,
        "key_decision_factors": ["DTI", "Credit Risk", "Stability Score"],
        "explanation": f"Preliminary decision is {classification} due to DTI {dti} and {credit_risk} risk."
    }