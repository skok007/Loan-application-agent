import streamlit as st
import pandas as pd
from pathlib import Path
import sys
import os

# Ensure root directory is on path
sys.path.append(os.path.abspath(".."))

from data_model import LoanApplicationJourney
from orchestrator_pipeline import orchestrate_application

st.set_page_config(page_title="Loan Summary Processor", layout="wide")
st.title("📄 Loan Application Summary Processor")

uploaded_file = st.file_uploader("Upload a CSV file with loan applications", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if not df.empty:
        st.success(f"Processing {len(df)} applications...")
        summaries = []

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
                    flagged_for_fraud=row["flagged_for_fraud"]
                )
                summary = orchestrate_application(app_data)
                summaries.append((app_data.application_id, summary))
            except Exception as e:
                summaries.append((row.get("application_id", f"Row {index}"), f"❌ Error: {e}"))

        for app_id, summary in summaries:
            st.markdown(f"### Application ID: `{app_id}`")
            st.markdown(summary)
            st.divider()
    else:
        st.warning("The uploaded file is empty.")