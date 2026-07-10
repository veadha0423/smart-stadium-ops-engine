import os
import requests
from dotenv import load_dotenv

load_dotenv()

class AIOperationalReasoner:
    def __init__(self):
        self.api_token = os.getenv("HF_API_TOKEN")
        # Updated to the primary stable Hugging Face Hub instruction model URL
        self.api_url = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
        self.headers = {"Authorization": f"Bearer {self.api_token}"}

    def generate_dispatch_instructions(self, sector: str, severity_score: float, raw_log: str) -> str:
        """Calls the serverless AI API to generate high-speed tactical instructions."""
        if not self.api_token:
            return "AI Operational Directive: Deploy sector emergency units immediately. (Fallback Mode: API Token Missing)"

        prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are the Lead AI Operational Commander at a major stadium event management center.
Analyze the following high-alert incident log and generate a precise, high-speed tactical dispatch instruction plan.

CRITICAL RULES:
1. Keep the output strictly under 4 lines total.
2. Provide an Executive Summary line, followed by exactly 3 clear, action-oriented bullet points.
3. Address specific facts from the log (e.g., location, injuries, personnel mentioned).
4. Do not include intro or outro conversational text.<|eot_id|><|start_header_id|>user<|end_header_id|>
[CRITICAL EMERGENCY SECTOR]: {sector} (Severity Matrix Score: {severity_score}/100)
[RAW LOG SEGMENT]:
{raw_log}

Operational Dispatch Directive Plan:<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 150,
                "temperature": 0.2,
                "return_full_text": False
            }
        }

        try:
            # Set a tight timeout constraint for rapid stadium operations
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=7)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and "generated_text" in result[0]:
                    return result[0]["generated_text"].strip()
                elif isinstance(result, dict) and "generated_text" in result:
                    return result["generated_text"].strip()
                return str(result)
                
            # If the specific model is loading or rate-limited, fall back to an elegant rule-based summary
            return self._generate_rule_based_fallback(sector, severity_score)
            
        except Exception:
            # Clean, elegant structural fallback if DNS or internet connection fails completely
            return self._generate_rule_based_fallback(sector, severity_score)

    def _generate_rule_based_fallback(self, sector: str, severity_score: float) -> str:
        """Guarantees a clean, intelligent response to the user even if network connection drops."""
        return (
            f"STADIUM COMMAND CENTER DIRECTIVE [AUTOMATED FALLBACK]\n"
            f"• CRITICAL CRITICAL ALERT: The {sector.upper()} sector has reached an extreme threat score of {severity_score}/100.\n"
            f"• DISPATCH ORDER: Immediately deploy localized supervisors and target field teams to clear sector bottlenecks.\n"
            f"• COMMUNICATION: Open direct audio channel links with central operations and log updates every 60 seconds."
        )