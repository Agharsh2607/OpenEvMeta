import httpx
import logging

logger = logging.getLogger(__name__)

async def make_hf_request(url: str, headers: dict, payload: dict) -> dict:
    """Asynchronous wrapper for robust HuggingFace execution"""
    async with httpx.AsyncClient() as client:
        try:
            # We enforce asynchronous fetching here for optimized backend execution
            response = await client.post(url, headers=headers, json=payload, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"HF API Error: {e}")
            return {"error": str(e)}
