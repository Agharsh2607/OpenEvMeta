from config.env import HF_TOKEN, API_BASE_URL, MODEL_NAME
from utils.apiHandler import make_hf_request

class AIService:
    def __init__(self):
        # Do not hardcode secrets, relying strictly on config/env bindings
        self.headers = {
            "Authorization": f"Bearer {HF_TOKEN}" if HF_TOKEN else ""
        }
        self.endpoint = f"{API_BASE_URL}/{MODEL_NAME}"
        
    async def process_inference(self, payload_prompt: str) -> dict:
        """Invokes HuggingFace processing returning structured UI JSON safely"""
        payload = {"inputs": payload_prompt}
        res = await make_hf_request(self.endpoint, self.headers, payload)
        return res
        
ai_service = AIService()
