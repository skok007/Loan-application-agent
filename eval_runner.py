import pandas as pd
import asyncio
from datetime import datetime
from data_model import LoanApplicationJourney
from orchestrator_pipeline import orchestrate_application
from utils.load_env import setup_environment
from utils.config_loader import ConfigLoader
from tools.synthesize_summary import synthesize_summary
from agents import RunContextWrapper

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
            flagged_for_fraud=row["flagged_for_fraud"],
            monthly_income=row.get("monthly_income"),
            monthly_costs=row.get("monthly_costs"),
            requested_amount=row.get("requested_amount"),
            monthly_debt=row.get("monthly_debt", 0.0)
        )
        records.append(record)
    return records


async def evaluate_applications():
    decision_stats = {"✅": 0, "⚠️": 0, "❌": 0}
    file_path = "data/loan_applications_large_enriched.csv"
    records = load_applications_from_csv(file_path)
    config_loader = ConfigLoader()

    for app in records:
        print(f"\n📄 Processing: {app.application_id}")
        report = orchestrate_application(app, config=config_loader)
        summary = synthesize_summary(RunContextWrapper(report))
        print(f"📢 Final Output for {app.application_id}:\n{summary['summary_text']}")
        decision = report.final_decision or "Unknown"
        if "✅" in decision:
            decision_stats["✅"] += 1
        elif "❌" in decision:
            decision_stats["❌"] += 1
        elif "⚠️" in decision:
            decision_stats["⚠️"] += 1

    print("\n📊 Final Decision Breakdown:")
    for symbol, count in decision_stats.items():
        print(f"{symbol}: {count}")

if __name__ == "__main__":
    asyncio.run(evaluate_applications())