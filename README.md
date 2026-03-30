# Voice Emotion Detection System

A Python-based voice emotion detection system using Hugging Face's pre-trained models to classify emotions from audio recordings.

## Features
- Detects 7 emotions: happy, sad, angry, neutral, fear, disgust, surprise
- Uses free Hugging Face models (no paid APIs)
- Supports .wav audio files
- **🎤 Live voice recording** - Record directly from microphone
- **🌐 Web interface** - Beautiful browser-based UI
- **🖥️ Desktop GUI** - Native application
- **💻 CLI interface** - Command-line tool
- Provides confidence scores for predictions
- Beginner-friendly with detailed comments

## Tech Stack
- Python 3.8+
- Hugging Face Transformers
- PyTorch
- librosa (audio processing)
- soundfile (audio I/O)

## Project Structure
```
voice-emotion-detection/
├── src/
│   ├── __init__.py
│   ├── emotion_detector.py    # Main detection logic
│   ├── audio_processor.py     # Audio preprocessing
│   └── utils.py               # Helper functions
├── models/                     # Downloaded models cache
├── sample_audio/              # Test audio files
├── requirements.txt           # Dependencies
├── main.py                    # Entry point
├── test_detector.py           # Testing script
└── README.md
```

## Installation

See INSTALLATION.md for detailed setup instructions.

## Usage

### Web App (Recommended)
```bash
python web_app.py
# Open http://localhost:5000 in browser
# Upload file OR record live audio
```

### Live Recording
```bash
# Record from microphone
python live_recorder.py

# Continuous recording
python live_recorder.py --continuous

# List audio devices
python live_recorder.py --list-devices
```

### Command Line
```bash
python main.py --audio sample_audio/test.wav
```

### Desktop GUI
```bash
python gui_simple.py
```

## Model Information

Primary model: `superb/hubert-large-superb-er`
- Size: ~300MB
- Accuracy: High
- Speed: Moderate on CPU

## Future Enhancements
- GUI interface (Tkinter/PyQt)
- Web app (Flask/FastAPI)
- Real-time emotion detection
- Multi-language support

## Author
Student Project - Voice Emotion Detection
