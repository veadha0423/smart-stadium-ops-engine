from pydantic import BaseModel
from typing import Dict, Optional

class TriageResponse(BaseModel):
    filename: str
    status: str
    primary_threat_sector: str
    departmental_logs: Dict[str, str]