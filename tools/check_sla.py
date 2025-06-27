from agents import function_tool, RunContextWrapper
from data_model import LoanApplicationJourney

@function_tool()
def check_sla(wrapper: RunContextWrapper[LoanApplicationJourney]) -> str:
    context = wrapper.context
    violations = [step for step, duration in context.processing_steps.items() if duration > 60]
    return f"SLA violations in: {', '.join(violations)}" if violations else "All steps within SLA."
