from fastapi import FastAPI, UploadFile, File, HTTPException
from app.core.parser import StadiumOpsParser
from app.core.math_engine import StadiumSeverityEngine
from app.services.ai_reasoner import AIOperationalReasoner
from app.schemas.stadium_schema import TriageResponse
import os
import shutil

app = FastAPI(
    title="Smart Stadium & Tournament Operations Server",
    description="Day 4: AI Operational Reasoner Active."
)

parser = StadiumOpsParser()
matrix_engine = StadiumSeverityEngine()
ai_engine = AIOperationalReasoner()

@app.post("/api/v1/incident-triage", response_model=TriageResponse)
async def triage_incident_endpoint(file: UploadFile = File(...)):
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB Limit
    file.file.seek(0, os.SEEK_END)
    file_size = file.file.tell()
    file.file.seek(0)  # Reset file pointer
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Security Exception: File profile exceeds 5MB limit.")
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid extension. Only PDF logs supported.")
        
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, file.filename)
    
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 1. Day 2 Parser Layer
        raw_text = parser.extract_raw_text(temp_file_path)
        segmented_logs = parser.segment_incident_log(raw_text)
        
        # 2. Day 3 Math Engine Layer
        severity_scores = matrix_engine.process_stadium_matrix(segmented_logs)
        primary_threat = max(severity_scores, key=severity_scores.get)
        highest_score = severity_scores[primary_threat]
        
        # 3. Day 4 AI Reasoner Layer
        target_log_text = segmented_logs.get(primary_threat, "")
        ai_directive = ai_engine.generate_dispatch_instructions(
            sector=primary_threat,
            severity_score=highest_score,
            raw_log=target_log_text
        )
        
        return {
            "filename": file.filename,
            "status": "Operational Triage Evaluated Successfully",
            "primary_threat_sector": primary_threat,
            "highest_severity_score": highest_score,
            "severity_matrix": severity_scores,
            "ai_dispatch_directive": ai_directive,
            "departmental_logs": segmented_logs
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Triage Engine Failure: {str(e)}")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)