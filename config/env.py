import os

HF_TOKEN = os.environ.get("HF_TOKEN", "")
API_BASE_URL = os.environ.get("API_BASE_URL", "https://api-inference.huggingface.co/models")
# Defaulting to a standard text generation/classification model format, dynamic at runtime via ENV
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt2")
