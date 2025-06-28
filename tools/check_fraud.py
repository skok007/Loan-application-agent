from agents import function_tool, RunContextWrapper
from data_model import LoanApplicationJourney

@function_tool()
def check_fraud(wrapper: RunContextWrapper[LoanApplicationJourney], config=None) -> str:
    return "⚠️ Fraud flag triggered" if wrapper.context.flagged_for_fraud else "No fraud indicators detected"
