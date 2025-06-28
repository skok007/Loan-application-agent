import streamlit as st
import pandas as pd
from pathlib import Path
import sys
import os

# Add root directory to sys.path for module resolution
ROOT = Path(__file__).resolve().parent.parent

import json
with open(os.path.join(ROOT, "config", "config.json")) as f:
    full_config = json.load(f)

sys.path.insert(0, str(ROOT))

from utils.config_loader import ConfigLoader

from data_model import LoanApplicationJourney
from orchestrator_pipeline import orchestrate_application

st.set_page_config(page_title="Loan Summary Processor", layout="wide")
st.title("📄 Loan Application Summary Processor")

st.sidebar.header("Configuration")
good_threshold = st.sidebar.slider("Good Affordability Max Ratio", 0.0, 1.0, 0.25)
moderate_threshold = st.sidebar.slider("Moderate Affordability Max Ratio", 0.0, 1.0, 0.4)

st.subheader("Manual Input for One Application")
manual_input = st.checkbox("Enable Manual Entry")
if manual_input:
    with st.form("manual_entry"):
        app_id = st.text_input("Application ID", "MANUAL-001")
        submitted = st.text_input("Submitted Time", "2025-06-01T09:00:00")
        reviewed = st.text_input("Reviewed Time", "2025-06-01T09:30:00")
        approved = st.text_input("Approved Time", "")
        rejected = st.text_input("Rejected Time", "")
        steps_str = st.text_input("Processing Steps (dict)", "{'KYC': 72, 'CreditCheck': 30}")
        fraud = st.checkbox("Flagged for Fraud", False)
        income = st.number_input("Monthly Income", 0.0)
        costs = st.number_input("Monthly Costs", 0.0)
        requested = st.number_input("Requested Amount", 0.0)
        debt = st.number_input("Monthly Debt", 0.0)
        submitted_form = st.form_submit_button("Run Evaluation")
    
    if submitted_form:
        try:
            from tools.synthesize_summary import synthesize_summary
            from agents import RunContextWrapper

            steps = eval(steps_str)
            app_data = LoanApplicationJourney(
                application_id=app_id,
                submitted_time=submitted,
                reviewed_time=reviewed,
                approved_time=approved or None,
                rejected_time=rejected or None,
                processing_steps=steps,
                flagged_for_fraud=fraud,
                monthly_income=income,
                monthly_costs=costs,
                requested_amount=requested,
                monthly_debt=debt
            )
            thresholds = [
                {"max_ratio": good_threshold, "label": "✅ Good affordability", "level": "approve"},
                {"max_ratio": moderate_threshold, "label": "⚠️ Moderate affordability", "level": "review"},
                {"max_ratio": 1.0, "label": "❌ Low affordability score", "level": "reject"}
            ]
            dynamic_config = ConfigLoader(overrides={
                "affordability_thresholds": thresholds,
                "recommendation_matrix": full_config["recommendation_matrix"]
            })
            result = orchestrate_application(app_data, config=dynamic_config)
            summary = synthesize_summary(RunContextWrapper(result))
            st.markdown(f"### Application ID: `{app_id}`")
            st.markdown(summary["summary_text"])
            st.dataframe(pd.DataFrame([{
                "Application ID": app_id,
                "SLA Result": result.sla_result,
                "Fraud Result": result.fraud_result,
                "Affordability": f"{result.affordability_result} ({result.affordability_level})",
                "Recommendation": result.recommendation,
                "Explanation": result.explanation,
                "Timestamp": result.timestamp,
                "Final Decision": result.final_decision
            }]))
            st.divider()
        except Exception as e:
            st.error(f"❌ Error in manual entry: {e}")

uploaded_file = st.file_uploader("Upload a CSV file with loan applications", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if not df.empty:
        st.success(f"Processing {len(df)} applications...")
        summaries = []

        thresholds = [
            {"max_ratio": good_threshold, "label": "✅ Good affordability", "level": "approve"},
            {"max_ratio": moderate_threshold, "label": "⚠️ Moderate affordability", "level": "review"},
            {"max_ratio": 1.0, "label": "❌ Low affordability score", "level": "reject"}
        ]
        dynamic_config = ConfigLoader(overrides={
            "affordability_thresholds": thresholds,
            "recommendation_matrix": full_config["recommendation_matrix"]
        })

        from tools.synthesize_summary import synthesize_summary
        from agents import RunContextWrapper

        for index, row in df.iterrows():
            try:
                steps = eval(row["processing_steps"]) if isinstance(row["processing_steps"], str) else row["processing_steps"]
                app_data = LoanApplicationJourney(
                    application_id=row["application_id"],
                    submitted_time=row["submitted_time"],
                    reviewed_time=row["reviewed_time"],
                    approved_time=row.get("approved_time"),
                    rejected_time=row.get("rejected_time"),
                    processing_steps=steps,
                    flagged_for_fraud=row["flagged_for_fraud"],
                    monthly_income=row.get("monthly_income"),
                    monthly_costs=row.get("monthly_costs"),
                    requested_amount=row.get("requested_amount"),
                    monthly_debt=row.get("monthly_debt", 0.0)
                )
                result = orchestrate_application(app_data, config=dynamic_config)
                summaries.append({
                    "Application ID": app_data.application_id,
                    "SLA Result": result.sla_result,
                    "Fraud Result": result.fraud_result,
                    "Affordability": f"{result.affordability_result} ({result.affordability_level})",
                    "Recommendation": result.recommendation,
                    "Explanation": result.explanation,
                    "Timestamp": result.timestamp,
                    "Final Decision": result.final_decision
                })
            except Exception as e:
                summaries.append({
                    "Application ID": row.get("application_id", f"Row {index}"),
                    "SLA Result": f"❌ Error: {e}",
                    "Fraud Result": "",
                    "Affordability": "",
                    "Recommendation": "",
                    "Explanation": "",
                    "Timestamp": ""
                })

        st.dataframe(pd.DataFrame(summaries))
    else:
        st.warning("The uploaded file is empty.")