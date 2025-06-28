from tools.check_sla import check_sla
from tools.check_fraud import check_fraud
from tools.check_audit_trail import check_audit_trail
from tools.explain_decision import explain_decision
from tools.synthesize_summary import synthesize_summary
from tools.check_affordability import check_affordability
from data_model import LoanApplicationJourney, TrendAnalysisResult
from agents import RunContextWrapper
from datetime import datetime


def orchestrate_application(app: LoanApplicationJourney, config=None) -> str:
    """
    Runs the full orchestration pipeline using explicit tool calls.
    Returns the final markdown report string.
    """
    wrapper = RunContextWrapper(app)

    # Step 1: Individual checks
    sla_result = check_sla(wrapper, config=config)
    fraud_result = check_fraud(wrapper, config=config)
    audit_result = check_audit_trail(wrapper, config=config)
    affordability_output = check_affordability(wrapper, config=config)
    affordability_label = affordability_output["label"]
    affordability_level = affordability_output["level"]

    # Step 2: High-level explanation based on SLA, fraud & affordability
    explanation = explain_decision(sla_result, fraud_result, affordability_label)

    # Step 3: Compile structured result for reporting
    report_context = TrendAnalysisResult(
        application_id=app.application_id,
        sla_result=sla_result,
        fraud_result=fraud_result,
        recommendation=f"{audit_result} | {affordability_label}",  # Optionally replace with rule-based logic
        explanation=explanation,
        affordability_result=affordability_label,
        affordability_level=affordability_level,
        timestamp=datetime.now().isoformat()
    )

    # Step 4: Create formatted report string
    return report_context