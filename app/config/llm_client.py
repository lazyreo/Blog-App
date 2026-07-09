from google import genai

from .settings import settings

api_key = settings.AI_API_KEY
client = genai.Client(api_key=api_key)
model = "gemini-3.1-flash-lite"
