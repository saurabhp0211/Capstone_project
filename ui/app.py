import streamlit as st
import requests
import uuid

# Configuration
API_URL = "http://localhost:8000/api/v1/loan/apply"

st.set_page_config(page_title="Agentic Loan Approver", layout="wide")
st.title("🏦 Agentic AI Intelligent Loan Approval")

st.markdown("""
Fill out the applicant details below. The multi-agent system will analyze the profile, evaluate financial risk, and use Claude 3.5 Sonnet to synthesize a final, explainable decision.
""")

# Input Form
with st.form("loan_application_form"):
    st.subheader("Applicant Details")
    
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=18, max_value=100, value=30)
        income = st.number_input("Annual Income ($)", min_value=10000, value=75000)
        employment_type = st.selectbox("Employment Type", ["Salaried", "Full-Time", "Self-Employed", "Part-Time", "Unemployed"])
        location = st.text_input("Location (City/State)", value="Bengaluru, KA") # <--- ADD THIS
        
    with col2:
        credit_score = st.number_input("Credit Score", min_value=300, max_value=850, value=720)
        loan_amount = st.number_input("Requested Loan Amount ($)", min_value=1000, value=25000)
        tenure = st.number_input("Loan Tenure (Months)", min_value=12, max_value=360, value=60)
        existing_liabilities = st.number_input("Existing Liabilities ($)", min_value=0, value=15000)

    submit_button = st.form_submit_button("Submit Application")

# Handling the Submission
if submit_button:
    # Build the payload matching the Pydantic schema
    payload = {
        "applicant_id": f"APP-{uuid.uuid4().hex[:6].upper()}",
        "age": age,
        "income": float(income),
        "employment_type": employment_type,
        "credit_score": credit_score,
        "loan_amount": float(loan_amount),
        "tenure": int(tenure),             
        "location": location,             
        "existing_liabilities": float(existing_liabilities)
    }
    
    with st.spinner("Agents are analyzing the application..."):
        try:
            # Send data to FastAPI
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                decision = data.get("decision", {})
                classification = decision.get("Classification", "Unknown")
                
                st.divider()
                st.subheader("🤖 Multi-Agent Decision Output")
                
                # Display dynamic status colors
                if classification.upper() == "APPROVED":
                    st.success(f"**Status:** {classification}")
                elif classification.upper() == "REJECTED":
                    st.error(f"**Status:** {classification}")
                else:
                    st.warning(f"**Status:** {classification}")
                
                # Metrics
                col3, col4 = st.columns(2)
                col3.metric("Risk Score", decision.get("Risk Score", "N/A"))
                col4.metric("Applicant ID", data.get("applicant_id"))
                
                # Explainable AI Output
                st.info(f"**AI Reasoning:** {decision.get('Explanation', 'No explanation provided.')}")
                
            else:
                st.error(f"API Error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the API. Make sure your FastAPI server is running!")