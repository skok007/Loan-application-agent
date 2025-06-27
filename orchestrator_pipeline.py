from tools.check_sla import check_sla
from tools.check_fraud import check_fraud
from tools.check_audit_trail import check_audit_trail
from tools.explain_decision import explain_decision
from tools.synthesize_summary import synthesize_summary
from data_model import LoanApplicationJourney, TrendAnalysisResult
from agents import RunContextWrapper
from datetime import datetime


def orchestrate_application(app: LoanApplicationJourney) -> str:
    """
    Runs the full orchestration pipeline using explicit tool calls.
    Returns the final markdown report string.
    """
    wrapper = RunContextWrapper(app)

    # Step 1: Individual checks
    sla_result = check_sla(wrapper)
    fraud_result = check_fraud(wrapper)
    audit_result = check_audit_trail(wrapper)

    # Step 2: High-level explanation based on SLA & fraud
    explanation = explain_decision(sla_result, fraud_result)

    # Step 3: Compile structured result for reporting
    report_context = TrendAnalysisResult(
        application_id=app.application_id,
        sla_result=sla_result,
        fraud_result=fraud_result,
        recommendation=audit_result,  # Optionally replace with rule-based logic
        explanation=explanation,
        timestamp=datetime.now().isoformat()
    )

    # Step 4: Create formatted report string
    return synthesize_summary(RunContextWrapper(report_context))