"""
Simple Flask Web App for Voice Emotion Detection
Run: python web_app.py
Then open: http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from src.emotion_detector import EmotionDetector
from src.audio_processor import AudioProcessor

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'temp_uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max

# Create upload folder
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)

# Initialize (lazy loading)
detector = None
processor = AudioProcessor()

def get_detector():
    global detector
    if detector is None:
        print("Loading model...")
        detector = EmotionDetector()
    return detector

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    file = request.files['audio']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Save file
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    try:
        # Process audio
        waveform, sr = processor.load_audio(filepath)
        waveform = processor.preprocess_audio(waveform, sr)
        
        # Predict
        det = get_detector()
        emotion, confidence, all_scores = det.predict(waveform, sr)
        
        # Clean up
        os.remove(filepath)
        
        # Emoji mapping
        emoji_map = {
            'happy': '😊', 'sad': '😢', 'angry': '😠',
            'neutral': '😐', 'fear': '😨', 'disgust': '🤢',
            'surprise': '😲', 'hap': '😊', 'ang': '😠',
            'neu': '😐'
        }
        
        return jsonify({
            'success': True,
            'emotion': emotion,
            'emoji': emoji_map.get(emotion.lower(), '🎭'),
            'confidence': float(confidence) * 100,
            'all_scores': {k: float(v) * 100 for k, v in all_scores.items()}
        })
        
    except Exception as e:
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎤 Voice Emotion Detection Web App")
    print("="*60)
    print("\n📱 Open in browser: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
