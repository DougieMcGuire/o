from flask import Flask, request, jsonify, send_from_directory
import os
import asyncio
import edge_tts

app = Flask(__name__)

# Directory to store generated files
OUTPUT_DIR = "static"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Generate audio using Edge TTS
async def generate_audio(text, voice, output_path):
    tts = edge_tts.Communicate(text, voice)
    await tts.save(output_path)

@app.route('/tts', methods=['POST'])
def tts():
    data = request.json
    text = data.get("text", "").strip()
    voice = data.get("voice", "en-US-AriaNeural")  # Default voice

    if not text:
        return jsonify({"error": "No text provided"}), 400

    filename = f"tts_output.mp3"
    output_path = os.path.join(OUTPUT_DIR, filename)

    # Run the TTS generation asynchronously
    asyncio.run(generate_audio(text, voice, output_path))

    return jsonify({"audio_url": f"/static/{filename}"})

# Endpoint to list available voices
@app.route('/voices', methods=['GET'])
async def list_voices():
    voices = await edge_tts.list_voices()
    return jsonify(voices)

# Serve static files (MP3)
@app.route('/static/<filename>')
def serve_static(filename):
    return send_from_directory(OUTPUT_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)
