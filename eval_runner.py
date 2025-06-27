import pandas as pd
import asyncio
from datetime import datetime
from data_model import LoanApplicationJourney
from orchestrator_pipeline import orchestrate_application
from utils.load_env import setup_environment

setup_environment()

def load_applications_from_csv(file_path):
    df = pd.read_csv(file_path)
    records = []
    for _, row in df.iterrows():
        steps = eval(row["processing_steps"]) if isinstance(row["processing_steps"], str) else row["processing_steps"]
        record = LoanApplicationJourney(
            application_id=row["application_id"],
            submitted_time=row["submitted_time"],
            reviewed_time=row["reviewed_time"],
            approved_time=row.get("approved_time"),
            rejected_time=row.get("rejected_time"),
            processing_steps=steps,
            flagged_for_fraud=row["flagged_for_fraud"]
        )
        records.append(record)
    return records


async def evaluate_applications():
    file_path = "data/loan_applications_large.csv"
    records = load_applications_from_csv(file_path)

    for app in records:
        print(f"\n📄 Processing: {app.application_id}")
        report = orchestrate_application(app)
        print("📢 Final Output:\n", report)

if __name__ == "__main__":
    asyncio.run(evaluate_applications())