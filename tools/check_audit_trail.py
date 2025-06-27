from agents import function_tool, RunContextWrapper
from data_model import LoanApplicationJourney
from datetime import datetime

@function_tool()
def check_audit_trail(wrapper: RunContextWrapper[LoanApplicationJourney]) -> str:
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

        if event_names != sorted(event_names):
            return f"⚠️ Audit warning: unexpected sequence - {event_names}"
        return "✅ Audit trail valid and sequential"
    except Exception as e:
        return f"Error in audit trail validation: {str(e)}"