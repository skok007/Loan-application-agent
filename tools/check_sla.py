from agents import function_tool, RunContextWrapper
from data_model import LoanApplicationJourney
from utils.config_loader import ConfigLoader

@function_tool()
def check_sla(wrapper: RunContextWrapper[LoanApplicationJourney], config=None) -> str:
    journey = wrapper.context
    thresholds = config.get_sla_thresholds() if config else {}

    violations = []
    for step, duration in journey.processing_steps.items():
        limit = thresholds.get(step, 60)  # fallback to default SLA of 60 if not specified
        if duration > limit:
            violations.append(step)

    if violations:
        return f"SLA violations in: {', '.join(violations)}"
    return "All steps within SLA."