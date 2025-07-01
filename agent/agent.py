import os
from dotenv import load_dotenv
import google.generativeai as genai
from backend.calendar_utils import get_free_slots, book_slot

# ✅ Load environment variables from .env
load_dotenv()

# ✅ Configure Gemini with secure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ✅ Initialize Gemini Pro model
model = genai.GenerativeModel("gemini-pro")

# ✅ Chat interface logic with basic intent handling
def chat_with_agent(user_input: str):
    try:
        user_input_lower = user_input.lower()

        # Basic intent matching — can be upgraded with Gemini parsing
        if "book" in user_input_lower and "july 3" in user_input_lower:
            return "✅ " + str(book_slot("2025-07-03", "10:30", "Consultation"))

        elif "slots" in user_input_lower or "appointments" in user_input_lower:
            return "📅 " + str(get_free_slots("2025-07-01"))

        else:
            # General LLM chat
            response = model.generate_content(user_input)
            return response.text

    except Exception as e:
        return f"⚠️ Error: {e}"
