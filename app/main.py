from fastapi import FastAPI, UploadFile, File, HTTPException
from app.core.parser import StadiumOpsParser
from app.schemas.stadium_schema import TriageResponse
import os
import shutil

app = FastAPI(
    title="Smart Stadium & Tournament Operations Server",
    description="Day 2: Multi-Channel Operational Parser Engine Active."
)

parser = StadiumOpsParser()

@app.post("/api/v1/parse-log", response_model=TriageResponse)
async def parse_log_endpoint(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid extension. Only PDF logs supported.")
        
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, file.filename)
    
    try:
        # Save incident streaming chunk securely into local sandbox
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Execute parsing pipeline 
        raw_text = parser.extract_raw_text(temp_file_path)
        segmented_logs = parser.segment_incident_log(raw_text)
        
        # Day 2 Placeholder logic: identify primary channel by density size
        primary_sector = max(segmented_logs, key=lambda k: len(segmented_logs[k]))
        
        return {
            "filename": file.filename,
            "status": "Logs Segregated Successfully",
            "primary_threat_sector": primary_sector,
            "departmental_logs": segmented_logs
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parser Crash: {str(e)}")
    finally:
        # Prevent disk footprint pollution by clearing local file copies
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)