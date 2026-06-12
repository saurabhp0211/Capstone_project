from mcp.server.fastmcp import FastMCP

mcp = FastMCP("RiskRulesDB")

@mcp.tool()
def calculate_risk(income: float, existing_liabilities: float, credit_score: int, loan_amount: float) -> dict:
    """Calculates financial risk metrics like DTI and credit score risk."""
    
    dti = existing_liabilities / income if income > 0 else 1.0
    
    if credit_score >= 750:
        risk_level = "Low"
    elif credit_score >= 650:
        risk_level = "Medium"
    else:
        risk_level = "High"
        
    loan_risk = "High" if loan_amount > (income * 5) else "Low"
    anomaly = "High DTI detected" if dti > 0.5 else "None"
    
    return {
        "debt_to_income_ratio": round(dti, 2),
        "credit_score_risk_level": risk_level,
        "loan_amount_risk": loan_risk,
        "anomaly_detection": anomaly,
        "reasoning": f"DTI is {dti:.2f}, Credit score is {credit_score}."
    }