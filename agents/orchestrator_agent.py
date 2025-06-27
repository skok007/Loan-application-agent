from agents import Agent
from tools.check_sla import check_sla
from tools.check_fraud import check_fraud
from tools.explain_decision import explain_decision
from tools.synthesize_summary import synthesize_summary
from tools.check_audit_trail import check_audit_trail
from data_model import LoanApplicationJourney, TrendAnalysisResult

orchestrator_agent = Agent[LoanApplicationJourney](
    name="LoanOrchestratorAgent",
    instructions=(
        "You are an orchestrator. Call check_sla, check_fraud, and check_audit_trail tools. "
        "Then call explain_decision and synthesize_summary to prepare the final report."
    ),
    tools=[check_sla, check_fraud, check_audit_trail, explain_decision, synthesize_summary],
    model="gpt-4-0613",
    output_type=str
)
