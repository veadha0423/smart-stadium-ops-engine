from pydantic import BaseModel
from typing import Dict

class TriageResponse(BaseModel):
    filename: str
    status: str
    primary_threat_sector: str
    highest_severity_score: float
    severity_matrix: Dict[str, float]
    ai_dispatch_directive: str  
    departmental_logs: Dict[str, str]