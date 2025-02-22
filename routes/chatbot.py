from flask import Blueprint, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Define Flask Blueprint
chatbot = Blueprint("chatbot", __name__)

# System Instruction to Keep Responses Relevant
PROMPT = """You are a chatbot for MovieFlix, an online movie ticket booking platform. 
You only answer questions related to movies, showtimes, ticket booking, and general customer queries related to MovieFlix.
If the user asks about something unrelated (e.g., politics, sports, technology), politely inform them that you can only assist with movies and ticket booking.
Keep your responses short and concise.
"""

@chatbot.route("/chatbot", methods=["POST"])
def chatbot_response():
    try:
        user_message = request.json.get("message")
        if not user_message:
            return jsonify({"response": "Please enter a message."})

        # Send request to Gemini AI with instructions
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(PROMPT + "\nUser: " + user_message + "\nBot:")

        # Get response text
        bot_response = response.text.strip()

        # If Gemini gives a long response, shorten it
        if len(bot_response) > 150:
            bot_response = bot_response[:147] + "..."

        return jsonify({"response": bot_response})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})
