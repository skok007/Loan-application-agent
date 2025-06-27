def explain_decision(sla_result: str, fraud_result: str) -> str:
    """
    Generate a simple explanation string based on SLA and fraud tool results.
    """
    if "violations" in sla_result and "Fraud" in fraud_result:
        return "Application has SLA delays and fraud indicators; high risk."
    elif "violations" in sla_result:
        return "Only SLA delays present; consider process efficiency."
    elif "Fraud" in fraud_result:
        return "Fraud flag triggered; requires escalation."
    return "No issues detected; eligible for fast-track approval."