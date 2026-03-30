# Voice Emotion Detection System

A Python-based voice emotion detection system using Hugging Face's pre-trained models to classify emotions from audio recordings.

## Features
- Detects 7 emotions: happy, sad, angry, neutral, fear, disgust, surprise
- Uses free Hugging Face models (no paid APIs)
- Supports .wav audio files
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

```python
python main.py --audio sample_audio/test.wav
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
