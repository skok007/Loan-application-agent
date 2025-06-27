
from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class LoanApplicationJourney:
    application_id: str
    submitted_time: str
    reviewed_time: str
    approved_time: Optional[str]
    rejected_time: Optional[str]
    processing_steps: Dict[str, int]
    flagged_for_fraud: bool

@dataclass
class TrendAnalysisResult:
    application_id: str
    sla_result: str
    fraud_result: str
    recommendation: str
    explanation: str
    timestamp: str