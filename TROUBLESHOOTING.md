# Troubleshooting Guide

## Common Issues and Solutions

### Installation Issues

#### Issue 1: "No module named 'torch'"
**Problem**: PyTorch not installed
**Solution**:
```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
```

#### Issue 2: "No module named 'transformers'"
**Problem**: Transformers library not installed
**Solution**:
```bash
pip install transformers
```

#### Issue 3: librosa installation fails
**Problem**: Missing system dependencies
**Solution (Linux)**:
```bash
sudo apt-get install libsndfile1 ffmpeg
pip install librosa
```
**Solution (Windows)**:
- Install Microsoft C++ Build Tools
- Then: `pip install librosa`

#### Issue 4: "ERROR: Could not build wheels for..."
**Problem**: Compilation issues
**Solution**:
```bash
# Use pre-built wheels
pip install --only-binary :all: librosa soundfile
```

### Runtime Issues

#### Issue 5: "Model download failed" or "Connection timeout"
**Problem**: Network issues or firewall
**Solution**:
- Check internet connection
- Try again (downloads can be interrupted)
- Use VPN if blocked
- Manually download model:
```python
from transformers import AutoModel
model = AutoModel.from_pretrained("superb/hubert-large-superb-er", 
                                   cache_dir="./models")
```

#### Issue 6: "CUDA out of memory"
**Problem**: GPU memory insufficient
**Solution**:
```bash
# Use CPU instead
python main.py --audio file.wav  # Don't use --gpu flag
```

#### Issue 7: "RuntimeError: Insufficient memory"
**Problem**: Not enough RAM
**Solution**:
- Close other applications
- Use lighter model:
```python
# In emotion_detector.py
MODEL_NAME = "speechbrain/emotion-recognition-wav2vec2-IEMOCAP"
```
- Process shorter audio clips

#### Issue 8: "Audio file not found"
**Problem**: Wrong file path
**Solution**:
```bash
# Use absolute path
python main.py --audio /full/path/to/audio.wav

# Or relative path from project root
python main.py --audio sample_audio/test.wav
```

#### Issue 9: "Unsupported audio format"
**Problem**: File format not supported
**Solution**:
- Convert to .wav using online converter or:
```bash
# Using ffmpeg
ffmpeg -i input.mp3 output.wav
```

#### Issue 10: "Audio too short" error
**Problem**: Audio less than 0.5 seconds
**Solution**:
- Use longer audio clip (3-10 seconds ideal)
- Record more speech

### Performance Issues

#### Issue 11: Very slow inference
**Problem**: CPU processing is slow
**Solutions**:
1. Use GPU if available: `--gpu` flag
2. Process shorter clips
3. Close other applications
4. Use lighter model

#### Issue 12: High memory usage
**Problem**: Model and audio in memory
**Solutions**:
- Process one file at a time
- Clear cache between runs
- Use model quantization:
```python
model = torch.quantization.quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8
)
```

### Accuracy Issues

#### Issue 13: Low confidence scores
**Problem**: Unclear audio or mixed emotions
**Solutions**:
- Use clearer recording
- Reduce background noise
- Speak more expressively
- Use better microphone
- Try different audio segment

#### Issue 14: Wrong emotion detected
**Problem**: Model misclassification
**Possible Causes**:
- Subtle emotion expression
- Cultural differences
- Background noise
- Poor audio quality
- Mixed emotions

**Solutions**:
- Record clearer audio
- Express emotion more clearly
- Try multiple recordings
- Check if emotion is in supported set

### Model Issues

#### Issue 15: "Model config not found"
**Problem**: Corrupted model cache
**Solution**:
```bash
# Clear cache and re-download
rm -rf ~/.cache/huggingface/
python main.py --audio test.wav  # Will re-download
```

#### Issue 16: Different results each time
**Problem**: This is normal for some models
**Solution**:
- Set random seed for reproducibility:
```python
import torch
torch.manual_seed(42)
```

### System-Specific Issues

#### Windows Issues

**Issue 17: "python: command not found"**
**Solution**: Use `python3` or `py` instead:
```bash
py main.py --audio test.wav
```

**Issue 18: Path issues with backslashes**
**Solution**: Use forward slashes or raw strings:
```python
path = r"C:\Users\Name\audio.wav"
# or
path = "C:/Users/Name/audio.wav"
```

#### Linux Issues

**Issue 19: Permission denied**
**Solution**:
```bash
chmod +x main.py
# or
python3 main.py --audio test.wav
```

#### Mac Issues

**Issue 20: "SSL: CERTIFICATE_VERIFY_FAILED"**
**Solution**:
```bash
# Install certificates
/Applications/Python\ 3.x/Install\ Certificates.command
```

### Debugging Steps

If you encounter an unknown error:

1. **Check Python version**:
```bash
python --version  # Should be 3.8+
```

2. **Verify all dependencies**:
```bash
pip list | grep -E "torch|transformers|librosa"
```

3. **Test with simple audio**:
```bash
python test_detector.py
```

4. **Enable verbose output**:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

5. **Check system resources**:
```bash
# Linux/Mac
free -h  # Check RAM
df -h    # Check disk space

# Windows
# Use Task Manager
```

6. **Try minimal example**:
```python
import torch
import transformers
import librosa
print("All imports successful!")
```

### Getting Help

If issues persist:

1. **Check error message carefully**
2. **Search error on Google/Stack Overflow**
3. **Check GitHub issues**: https://github.com/huggingface/transformers/issues
4. **Ask on forums**:
   - Hugging Face forums
   - Stack Overflow
   - Reddit r/MachineLearning

5. **Provide details when asking**:
   - Python version
   - OS and version
   - Full error message
   - Steps to reproduce
   - What you've tried

### Prevention Tips

1. **Use virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. **Keep dependencies updated**:
```bash
pip install --upgrade pip
pip install --upgrade -r requirements.txt
```

3. **Test after installation**:
```bash
python test_detector.py
```

4. **Use version control**:
```bash
git init
git add .
git commit -m "Initial commit"
```

5. **Document your environment**:
```bash
pip freeze > requirements_frozen.txt
```
