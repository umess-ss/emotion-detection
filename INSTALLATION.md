# Installation Guide

## Step 1: Check Python Version
```bash
python --version
# Should be Python 3.8 or higher
```

If you don't have Python 3.8+, download from: https://www.python.org/downloads/

## Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

## Step 3: Install Dependencies
```bash
# Upgrade pip first
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

### If you face issues:

**For PyTorch installation issues:**
```bash
# CPU-only version (lighter, recommended for laptops)
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
```

**For librosa issues on Linux:**
```bash
sudo apt-get install libsndfile1
```

**For Windows users:**
- Install Microsoft C++ Build Tools if you get compilation errors
- Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

## Step 4: Verify Installation
```bash
python -c "import torch; import transformers; import librosa; print('All dependencies installed successfully!')"
```

## Step 5: Test the System
```bash
# Run the test script
python test_detector.py
```

## Troubleshooting

### Low RAM Issues
If your system has <4GB RAM, use the lighter model by editing `src/emotion_detector.py`:
```python
MODEL_NAME = "ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition"
```

### Slow Performance
- Use CPU-only PyTorch (smaller download)
- Close other applications while running
- Process shorter audio clips (<10 seconds)

### Model Download Issues
- Ensure stable internet connection
- Models are cached in `~/.cache/huggingface/`
- First run will take time to download (~300MB)

## System Requirements

**Minimum:**
- Python 3.8+
- 4GB RAM
- 2GB free disk space
- Internet (first run only)

**Recommended:**
- Python 3.9+
- 8GB RAM
- 5GB free disk space
