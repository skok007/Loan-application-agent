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
    sla_result_obj = check_sla(wrapper, config=config)
    fraud_result_obj = check_fraud(wrapper, config=config)
    audit_result_obj = check_audit_trail(wrapper, config=config)
    affordability_output = check_affordability(wrapper, config=config)

    sla_result = sla_result_obj["label"]
    fraud_result = fraud_result_obj["label"]
    audit_result = audit_result_obj["label"]
    affordability_label = affordability_output["label"]
    affordability_level = affordability_output["level"]

    normalized_affordability = affordability_level.lower().strip()
    fraud_flagged = fraud_result_obj.get("flagged", False)
    sla_violation = sla_result_obj.get("violated", False)

    print(f"Matching with: affordability={normalized_affordability}, fraud={fraud_flagged}, sla={sla_violation}")

    final_decision = "Undetermined"
    for rule in config.get_recommendation_matrix():
        if (rule["affordability"] == normalized_affordability and
            rule["fraud"] == fraud_flagged and
            rule["sla_violation"] == sla_violation):
            final_decision = rule["decision"]
            break

    # Step 2: High-level explanation based on SLA, fraud & affordability
    explanation_output = explain_decision(sla_result_obj, fraud_result_obj, affordability_output)
    explanation = explanation_output["explanation"]

    # Step 3: Compile structured result for reporting
    report_context = TrendAnalysisResult(
        application_id=app.application_id,
        sla_result=sla_result,
        fraud_result=fraud_result,
        recommendation=f"{audit_result} | {affordability_label}",  # Optionally replace with rule-based logic
        explanation=explanation,
        affordability_result=affordability_label,
        affordability_level=affordability_level,
        timestamp=datetime.now().isoformat(),
        final_decision=final_decision
    )

    # Step 4: Create formatted report string
    return report_context