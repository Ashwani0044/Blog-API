from flask import Blueprint, request, jsonify
from google import genai
# from openai import OpenAI
import os

ai_bp = Blueprint('ai', __name__)

# client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# @ai_bp.route('/generate-caption', methods=['POST'])
# def generate_caption():
#     data = request.get_json()
#     content = data.get('content')

#     if not content:
#         return jsonify({'error': 'Content is required'}), 400
    
#     try:
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#              messages=[
#                 {"role": "system", "content": "You are a creative social media assistant."},
#                 {"role": "user", "content": f"Generate a catchy Instagram caption for: {content}"}
#             ],
#             max_tokens=50
#         )
#         caption = response.choices[0].message.content.strip()

#         return jsonify({'caption': caption})
    
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


@ai_bp.route("/generate-caption", methods=["POST"])
def generate_caption():
    data = request.get_json()
    content = data.get('content')

    if not content:
        return jsonify(message="Content required"), 400

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"""
Generate ONLY ONE short Instagram caption (max 10 words) with emojis.
Do not give multiple options. Do not number anything.

Content: {content}
"""
        )

        return jsonify(caption=response.text.strip())

    except Exception as e:
        return jsonify(error=str(e)), 500