# Deployment Guide

## Desktop Application (GUI)

### Option 1: Tkinter (Built-in Python)

Create `gui_tkinter.py`:

```python
import tkinter as tk
from tkinter import filedialog, messagebox
from src.emotion_detector import EmotionDetector
from src.audio_processor import AudioProcessor

class EmotionDetectorGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Voice Emotion Detector")
        self.detector = None
        self.audio_processor = AudioProcessor()
        
        # Create UI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title = tk.Label(self.window, text="🎤 Voice Emotion Detector", 
                        font=("Arial", 20))
        title.pack(pady=20)
        
        # Select file button
        self.select_btn = tk.Button(self.window, text="Select Audio File",
                                    command=self.select_file)
        self.select_btn.pack(pady=10)
        
        # Result label
        self.result_label = tk.Label(self.window, text="", 
                                     font=("Arial", 16))
        self.result_label.pack(pady=20)
        
    def select_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Audio Files", "*.wav *.mp3")]
        )
        if file_path:
            self.process_audio(file_path)
    
    def process_audio(self, file_path):
        try:
            # Load model if not loaded
            if not self.detector:
                self.result_label.config(text="Loading model...")
                self.window.update()
                self.detector = EmotionDetector()
            
            # Process audio
            waveform, sr = self.audio_processor.load_audio(file_path)
            waveform = self.audio_processor.preprocess_audio(waveform, sr)
            
            # Predict
            emotion, confidence, _ = self.detector.predict(waveform, sr)
            
            # Show result
            result_text = f"Emotion: {emotion.upper()}\nConfidence: {confidence*100:.1f}%"
            self.result_label.config(text=result_text)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = EmotionDetectorGUI()
    app.run()
```

Run: `python gui_tkinter.py`

### Option 2: PyQt5 (More Professional)

Install: `pip install PyQt5`

Similar structure but with more features:
- Drag and drop
- Progress bars
- Better styling
- Menu bars

### Creating Executable

Using PyInstaller:

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed --name "EmotionDetector" main.py

# Executable will be in dist/ folder
```

## Web Application

### Option 1: Flask (Simple)

Create `app_flask.py`:

```python
from flask import Flask, request, render_template, jsonify
from src.emotion_detector import EmotionDetector
from src.audio_processor import AudioProcessor
import os

app = Flask(__name__)
detector = EmotionDetector()
processor = AudioProcessor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file'}), 400
    
    file = request.files['audio']
    filepath = f"temp/{file.filename}"
    file.save(filepath)
    
    try:
        waveform, sr = processor.load_audio(filepath)
        waveform = processor.preprocess_audio(waveform, sr)
        emotion, confidence, scores = detector.predict(waveform, sr)
        
        os.remove(filepath)
        
        return jsonify({
            'emotion': emotion,
            'confidence': float(confidence),
            'all_scores': {k: float(v) for k, v in scores.items()}
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    os.makedirs('temp', exist_ok=True)
    app.run(debug=True)
```

Create `templates/index.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Voice Emotion Detector</title>
</head>
<body>
    <h1>🎤 Voice Emotion Detector</h1>
    <form id="uploadForm">
        <input type="file" id="audioFile" accept="audio/*">
        <button type="submit">Analyze</button>
    </form>
    <div id="result"></div>
    
    <script>
        document.getElementById('uploadForm').onsubmit = async (e) => {
            e.preventDefault();
            const formData = new FormData();
            formData.append('audio', document.getElementById('audioFile').files[0]);
            
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            document.getElementById('result').innerHTML = 
                `<h2>Emotion: ${data.emotion}</h2>
                 <p>Confidence: ${(data.confidence * 100).toFixed(2)}%</p>`;
        };
    </script>
</body>
</html>
```

Run: `python app_flask.py`

### Option 2: FastAPI (Modern, Fast)

```bash
pip install fastapi uvicorn python-multipart
```

Similar to Flask but with automatic API documentation.

### Deployment to Cloud

#### Heroku (Free Tier)
1. Create `Procfile`: `web: gunicorn app_flask:app`
2. Create `runtime.txt`: `python-3.9.16`
3. Push to Heroku

#### AWS/Google Cloud
- Use Docker container
- Deploy to EC2/Compute Engine
- Use load balancer for scaling

## Android Application

### Option 1: Kivy (Python)

```bash
pip install kivy buildozer
```

Create cross-platform mobile app in Python.

### Option 2: React Native + Python Backend

1. Build Flask API (above)
2. Create React Native frontend
3. Call API from mobile app

### Option 3: Native Android (Java/Kotlin)

1. Export model to TensorFlow Lite
2. Build native Android app
3. Run inference on device

## API Service

Create REST API for integration:

```python
# api.py
from fastapi import FastAPI, File, UploadFile
from src.emotion_detector import EmotionDetector

app = FastAPI()
detector = EmotionDetector()

@app.post("/api/v1/detect")
async def detect_emotion(audio: UploadFile = File(...)):
    # Process and return result
    pass
```

Deploy to:
- AWS Lambda (serverless)
- Google Cloud Functions
- Azure Functions
- Docker container

## Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app_flask.py"]
```

Build and run:
```bash
docker build -t emotion-detector .
docker run -p 5000:5000 emotion-detector
```
