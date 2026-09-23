import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.0-flash"
)

try:
    response = model.generate_content(
        "Say hello."
    )

    print(response.text)

except Exception as e:
    print(e)