import re
import math

class StadiumSeverityEngine:
    def __init__(self):
        # Operational threat levels mapped to specific heavy keywords
        self.threat_weights = {
            "critical": {
                "keywords": ["fire", "smoke", "injury", "medical", "weapon", "fight", "breach", "stampede", "collapse", "blackout"],
                "multiplier": 2.5
            },
            "moderate": {
                "keywords": ["gate", "turnstile", "queue", "delay", "leak", "cleaning", "wifi", "network", "camera", "var"],
                "multiplier": 1.2
            }
        }

    def calculate_channel_severity(self, text_log: str) -> float:
        """
        Calculates a deterministic risk metric from 10.00 to 100.00 for a text block.
        Implements a logarithmic saturation curve to prevent keyword stuffing exploits.
        """
        if not text_log.strip():
            return 10.00  # Baseline safe score for an inactive or clear department
            
        base_score = 10.00
        critical_hits = 0
        moderate_hits = 0
        
        text_clean = text_log.lower()
        
        # Count structural matches
        for word in self.threat_weights["critical"]["keywords"]:
            critical_hits += text_clean.count(word)
            
        for word in self.threat_weights["moderate"]["keywords"]:
            moderate_hits += text_clean.count(word)
            
        # Mathematical Escalation Logic using logarithmic dampening
        # Score = Base + (Critical_Factor * ln(hits + 1)) + (Moderate_Factor * ln(hits + 1))
        critical_factor = 30.0 * self.threat_weights["critical"]["multiplier"]  # Max steepness 75
        moderate_factor = 15.0 * self.threat_weights["moderate"]["multiplier"]  # Max steepness 18
        
        escalation = (critical_factor * math.log(critical_hits + 1)) + (moderate_factor * math.log(moderate_hits + 1))
        
        final_score = base_score + escalation
        
        # Clamp bounds strictly between 10.00 and 100.00
        return round(min(100.00, max(10.00, final_score)), 2)

    def process_stadium_matrix(self, segmented_logs: dict) -> dict:
        """Computes severity matrix profiles across all active streaming channels."""
        matrix_scores = {}
        for department, text in segmented_logs.items():
            if department == "unclassified_ops":
                continue
            matrix_scores[department] = self.calculate_channel_severity(text)
        return matrix_scores