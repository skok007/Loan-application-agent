from utils.config_loader import ConfigLoader


def explain_decision(sla_result: str, fraud_result: str, affordability_result: str = "") -> str:
    templates = ConfigLoader().get_explanation_templates()

    if "Low affordability" in affordability_result:
        return templates.get("low_affordability", affordability_result)
    elif "violations" in sla_result and "Fraud" in fraud_result:
        return templates.get("fraud_flagged", fraud_result) + " " + templates.get("sla_violation", sla_result)
    elif "violations" in sla_result:
        return templates.get("sla_violation", sla_result)
    elif "Fraud" in fraud_result:
        return templates.get("fraud_flagged", fraud_result)
    return templates.get("clean", "No issues detected.")