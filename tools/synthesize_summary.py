from agents import function_tool, RunContextWrapper
from data_model import TrendAnalysisResult

@function_tool(strict_mode=False)
def synthesize_summary(wrapper: RunContextWrapper[TrendAnalysisResult]) -> str:
    r = wrapper.context
    return f"""
✉️ **Loan Decision Summary**
- Application ID: {r.application_id}
- SLA Result: {r.sla_result}
- Fraud Result: {r.fraud_result}
- Recommendation: {r.recommendation}
- Explanation: {r.explanation}
- Timestamp: {r.timestamp}
"""
