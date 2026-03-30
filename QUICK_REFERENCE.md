# Quick Reference Guide

## 🚀 Installation (One Command)

```bash
pip install torch transformers librosa soundfile numpy scipy
```

## 📝 Basic Usage

### Command Line
```bash
# Basic
python main.py --audio your_audio.wav

# With GPU
python main.py --audio your_audio.wav --gpu

# Different model
python main.py --audio your_audio.wav --model "speechbrain/emotion-recognition-wav2vec2-IEMOCAP"

# Show system info
python main.py --audio your_audio.wav --info
```

### Python Code
```python
from src.emotion_detector import EmotionDetector
from src.audio_processor import AudioProcessor

# Initialize
processor = AudioProcessor()
detector = EmotionDetector()

# Load and process audio
waveform, sr = processor.load_audio("audio.wav")
waveform = processor.preprocess_audio(waveform, sr)

# Predict
emotion, confidence, all_scores = detector.predict(waveform, sr)

print(f"Emotion: {emotion}")
print(f"Confidence: {confidence*100:.1f}%")
```

## 🎯 Common Commands

```bash
# Test system
python test_detector.py

# Launch GUI
python gui_simple.py

# Check Python version
python --version

# List installed packages
pip list

# Update dependencies
pip install --upgrade -r requirements.txt
```

## 🔧 Quick Fixes

### Model won't download
```bash
# Check internet
ping huggingface.co

# Clear cache and retry
rm -rf ~/.cache/huggingface/
python main.py --audio test.wav
```

### Out of memory
```python
# Use lighter model in emotion_detector.py
MODEL_NAME = "speechbrain/emotion-recognition-wav2vec2-IEMOCAP"
```

### Slow performance
```bash
# Use GPU if available
python main.py --audio test.wav --gpu

# Or process shorter clips
```

## 📊 Supported Formats

- ✅ .wav (recommended)
- ✅ .mp3
- ✅ .flac
- ✅ .ogg

## 🎤 Recording Audio

### Audacity (Free)
1. Download: audacityteam.org
2. Record (red button)
3. Export as WAV

### Python
```python
import sounddevice as sd
import soundfile as sf

# Record 5 seconds
audio = sd.rec(int(5 * 16000), samplerate=16000, channels=1)
sd.wait()
sf.write('recording.wav', audio, 16000)
```

## 🎭 Emotion Labels

1. happy 😊
2. sad 😢
3. angry 😠
4. neutral 😐
5. fear 😨
6. disgust 🤢
7. surprise 😲

## 📈 Confidence Levels

- **>70%**: HIGH - Very reliable
- **40-70%**: MEDIUM - Likely correct
- **<40%**: LOW - Uncertain

## 🔄 Model Switching

```python
# In emotion_detector.py, change line 18:

# Default (balanced)
MODEL_NAME = "superb/hubert-large-superb-er"

# Lighter (faster)
MODEL_NAME = "speechbrain/emotion-recognition-wav2vec2-IEMOCAP"

# Best accuracy (slower)
MODEL_NAME = "ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition"
```

## 🐛 Debugging

```python
# Enable verbose output
import logging
logging.basicConfig(level=logging.DEBUG)

# Check imports
import torch, transformers, librosa
print("All imports OK!")

# Check model
detector = EmotionDetector()
print(detector.get_model_info())
```

## 📁 File Structure

```
voice-emotion-detection/
├── src/                    # Source code
│   ├── emotion_detector.py # Model
│   ├── audio_processor.py  # Audio
│   └── utils.py           # Helpers
├── main.py                # CLI
├── gui_simple.py          # GUI
├── test_detector.py       # Tests
└── requirements.txt       # Dependencies
```

## 💻 System Requirements

**Minimum:**
- Python 3.8+
- 4GB RAM
- 2GB disk space

**Recommended:**
- Python 3.9+
- 8GB RAM
- 5GB disk space

## 🌐 Deployment Quick Start

### Flask Web App
```python
from flask import Flask, request, jsonify
from src.emotion_detector import EmotionDetector

app = Flask(__name__)
detector = EmotionDetector()

@app.route('/predict', methods=['POST'])
def predict():
    # Handle file upload and predict
    pass

app.run()
```

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

## 📚 Documentation Files

- **README.md** - Start here
- **INSTALLATION.md** - Setup guide
- **USAGE_GUIDE.md** - How to use
- **ARCHITECTURE.md** - Technical details
- **TROUBLESHOOTING.md** - Fix issues
- **VIVA_QUESTIONS.md** - Interview prep
- **MODEL_COMPARISON.md** - Choose model
- **QUICK_REFERENCE.md** - This file

## 🎓 Learning Path

1. Read README.md
2. Install (INSTALLATION.md)
3. Run test_detector.py
4. Try your audio
5. Read ARCHITECTURE.md
6. Explore code
7. Try improvements
8. Deploy

## 🔗 Useful Links

- Hugging Face: https://huggingface.co
- PyTorch: https://pytorch.org
- librosa: https://librosa.org
- Transformers Docs: https://huggingface.co/docs/transformers

## ⚡ Performance Tips

1. Use GPU for faster inference
2. Process shorter clips (3-10s)
3. Use lighter model for speed
4. Close other applications
5. Use CPU-only PyTorch if no GPU

## 🎯 Best Practices

### Audio Quality
- Clear speech
- Minimal background noise
- 3-10 seconds duration
- 16kHz sample rate
- Mono channel

### Code
- Use virtual environment
- Keep dependencies updated
- Test after changes
- Document modifications
- Use version control

## 🆘 Getting Help

1. Check TROUBLESHOOTING.md
2. Read error message carefully
3. Search on Google/Stack Overflow
4. Check GitHub issues
5. Ask on forums

## 📊 Quick Stats

- **Setup Time**: 5-10 minutes
- **First Run**: 2-5 minutes (model download)
- **Inference**: 1-5 seconds
- **Accuracy**: 70-85%
- **Supported Emotions**: 7

## ✅ Checklist

Before running:
- [ ] Python 3.8+ installed
- [ ] Dependencies installed
- [ ] Audio file ready
- [ ] Internet connection (first run)
- [ ] 4GB+ RAM available

## 🎉 Success Indicators

✓ Model loads without errors
✓ Audio processes successfully
✓ Predictions have >40% confidence
✓ Results make sense
✓ No error messages

## 🔮 Next Steps

After basic usage:
1. Try different audio samples
2. Test different models
3. Create GUI version
4. Deploy as web app
5. Add to portfolio
6. Prepare for interviews

---

**Need more details?** Check the specific documentation files!

**Quick help:** `python main.py --help`
