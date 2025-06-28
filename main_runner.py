import asyncio
from data_model import LoanApplicationJourney
from orchestrator_pipeline import orchestrate_application
#from agents.report_agent import report_agent, mcp_server
from agents import RunContextWrapper
from data_model import TrendAnalysisResult
from datetime import datetime
from utils.config_loader import ConfigLoader
from tools.synthesize_summary import synthesize_summary


async def run_pipeline(app: LoanApplicationJourney):
    # Step 1: Run full tool-based orchestration and get final summary string
    config = ConfigLoader()
    report = orchestrate_application(app, config=config)

    # Step 2: Build context for report agent (MCP optional)
    report_context = report

    # Step 3: Send report via MCP (optional toggle)
    send_to_mcp = False  # ✅ Change to True when ready

    if send_to_mcp:
        await mcp_server.__aenter__()
        final = await report_agent.run(input="Send report", context=report)
        await mcp_server.__aexit__(None, None, None)
        print("\n✅ Report sent via MCP:\n", final.final_output)
    else:
        print("\n📋 Final Report (Local Only):\n")
        summary = synthesize_summary(RunContextWrapper(report))
        print(summary["summary_text"])


if __name__ == "__main__":
    test_app = LoanApplicationJourney(
        application_id="APP-LOCAL-001",
        submitted_time="2025-06-01T09:00:00",
        reviewed_time="2025-06-01T09:30:00",
        approved_time="2025-06-01T10:00:00",
        rejected_time=None,
        processing_steps={"KYC": 72, "CreditCheck": 28, "FinalApproval": 35},
        flagged_for_fraud=False,
        monthly_income=5000,
        monthly_costs=2000,
        requested_amount=25000,
        monthly_debt=400
    )

    asyncio.run(run_pipeline(test_app))