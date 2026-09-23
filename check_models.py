import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

try:
    print("Checking models...\n")

    for model in genai.list_models():
        print(model.name)

except Exception as e:
    print(e)