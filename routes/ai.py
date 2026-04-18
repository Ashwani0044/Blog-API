from flask import Blueprint, request, jsonify
from openai import OpenAI
import os

ai_bp = Blueprint('ai', __name__)

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@ai_bp.route('/generate-caption', methods=['POST'])
def generate_caption():
    data = request.get_json()
    content = data.get('content')

    if not content:
        return jsonify({'error': 'Content is required'}), 400
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
             messages=[
                {"role": "system", "content": "You are a creative social media assistant."},
                {"role": "user", "content": f"Generate a catchy Instagram caption for: {content}"}
            ],
            max_tokens=50
        )
        caption = response.choices[0].message.content.strip()

        return jsonify({'caption': caption})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500