import re
import pdfplumber

class StadiumOpsParser:
    def __init__(self):
        # High-impact regex anchors tailored for stadium environments
        self.sections = {
            "crowd_control": re.compile(r'(crowd|gate|turnstile|seating|capacity|queue|stand|ticket|entry|exit|flux)', re.IGNORECASE),
            "security_emergency": re.compile(r'(security|medical|fire|emergency|police|hazard|fight|injury|smoke|breach|arrest)', re.IGNORECASE),
            "logistics_vendors": re.compile(r'(vendor|concession|food|cleaning|waste|parking|beverage|restroom|supply)', re.IGNORECASE),
            "technical_broadcast": re.compile(r'(broadcast|camera|screen|audio|lighting|wifi|network|var|comm|power|generator)', re.IGNORECASE)
        }

    def extract_raw_text(self, pdf_path: str) -> str:
        """Extracts text cleanly across all pages of an operational PDF log."""
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        return text

    def segment_incident_log(self, raw_text: str) -> dict:
        """Slices unstructured logs into departmental data streams deterministically."""
        lines = raw_text.split('\n')
        parsed_data = {key: "" for key in self.sections.keys()}
        parsed_data["unclassified_ops"] = ""
        
        current_section = "unclassified_ops"
        
        for line in lines:
            clean_line = line.strip()
            if not clean_line:
                continue
                
            # Scan if line triggers a channel context switch
            matched_new_section = False
            for section_name, regex in self.sections.items():
                # If keyword matches and line is a short header descriptor
                if regex.search(clean_line) and len(clean_line) < 45:
                    current_section = section_name
                    matched_new_section = True
                    break
            
            if matched_new_section:
                continue
                
            # Append log line to active structural channel context
            parsed_data[current_section] += line + "\n"
            
        return parsed_data