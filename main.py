from flask import Flask, request, send_file, jsonify
import edge_tts
import asyncio
import os
import tempfile
import time

app = Flask(__name__)

@app.route('/generate-speech', methods=['POST'])
def generate_speech():
    try:
        # Get JSON data from request
        data = request.json
        
        # Extract text and voice from request
        text = data.get('text')
        voice = data.get('voice')
        
        if not text or not voice:
            return jsonify({"error": "Missing 'text' or 'voice' parameter"}), 400
        
        # Generate a unique filename for this request
        output_file = os.path.join(tempfile.gettempdir(), f"speech_{int(time.time())}.mp3")
        
        # Run the async TTS generation function
        asyncio.run(generate_tts(text, voice, output_file))
        
        # Return the generated audio file
        return send_file(output_file, mimetype="audio/mpeg", as_attachment=True)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

async def generate_tts(text, voice, output_file):
    """Generate TTS audio file using Edge-TTS"""
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

@app.route('/list-voices', methods=['GET'])
def list_voices():
    """Endpoint to list all available voices"""
    try:
        # Run the async function to get voices
        voices = asyncio.run(get_voices())
        return jsonify(voices)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

async def get_voices():
    """Get list of available voices from Edge-TTS"""
    voices = await edge_tts.list_voices()
    return [{"name": voice["Name"], "locale": voice["Locale"]} for voice in voices]

if __name__ == '__main__':
    app.run(debug=True)
