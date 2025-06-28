from agents import function_tool, RunContextWrapper
from data_model import LoanApplicationJourney
from datetime import datetime

@function_tool()
def check_audit_trail(wrapper: RunContextWrapper[LoanApplicationJourney], config=None) -> str:
    journey = wrapper.context
    events = {
        "submitted": journey.submitted_time,
        "reviewed": journey.reviewed_time,
        "approved": journey.approved_time,
        "rejected": journey.rejected_time,
    }

    # Only include steps that exist and are strings
    timeline = [(k, v) for k, v in events.items() if isinstance(v, str)]

    try:
        parsed = [(k, datetime.fromisoformat(v)) for k, v in timeline]
        sorted_events = sorted(parsed, key=lambda x: x[1])
        event_names = [e[0] for e in sorted_events]

        expected_order = ["submitted", "reviewed", "approved", "rejected"]
        actual = event_names
        expected = [step for step in expected_order if step in actual]

        if actual != expected:
            return f"⚠️ Audit warning: unexpected sequence - {actual}"
        return "✅ Audit trail valid and sequential"
    except Exception as e:
        return f"Error in audit trail validation: {str(e)}"