# 🎤 Live Voice Recording Guide

## Overview

The system now supports **live voice recording** in three ways:
1. **Web App** - Record directly in browser
2. **Command Line** - Record from terminal
3. **Desktop GUI** - Record in desktop app (coming soon)

---

## 🌐 Web App Live Recording

### How to Use

1. **Start the web app**:
   ```bash
   source venv/bin/activate
   python web_app.py
   ```

2. **Open browser**: http://localhost:5000

3. **Click "🎤 Record Live Audio"**

4. **Allow microphone access** when prompted

5. **Speak** while recording (button shows "⏹️ Stop Recording")

6. **Click "⏹️ Stop Recording"** when done

7. **Click "Analyze Emotion"** to see results

### Features
- ✅ Browser-based recording
- ✅ No file upload needed
- ✅ Real-time capture
- ✅ Visual recording indicator
- ✅ Works on any device with microphone

---

## 💻 Command Line Live Recording

### Basic Usage

```bash
source venv/bin/activate
python live_recorder.py
```

This will:
- Record 5 seconds of audio
- Save to `recordings/` folder
- Analyze and show emotion

### Custom Duration

```bash
# Record for 10 seconds
python live_recorder.py --duration 10

# Record for 3 seconds
python live_recorder.py --duration 3
```

### List Audio Devices

```bash
python live_recorder.py --list-devices
```

Output:
```
🎤 Available Audio Devices:

  [0] Built-in Microphone
      Channels: 2
      Sample Rate: 44100.0

  [1] USB Microphone
      Channels: 1
      Sample Rate: 48000.0
```

### Use Specific Device

```bash
python live_recorder.py --device 1
```

### Continuous Recording Mode

```bash
# Keep recording and analyzing
python live_recorder.py --continuous

# Press Ctrl+C to stop
```

### Don't Save Recording

```bash
# Analyze without saving
python live_recorder.py --no-save
```

---

## 📋 Command Reference

### live_recorder.py Options

```bash
python live_recorder.py [OPTIONS]

Options:
  --duration SECONDS      Recording duration (default: 5)
  --device INDEX         Audio device index
  --list-devices         Show available devices
  --no-save              Don't save recording
  --continuous           Keep recording
  -h, --help             Show help
```

### Examples

```bash
# Quick 3-second recording
python live_recorder.py --duration 3

# Use USB mic, record 10 seconds
python live_recorder.py --device 1 --duration 10

# Continuous mode with 5-second clips
python live_recorder.py --continuous --duration 5

# Record without saving
python live_recorder.py --no-save
```

---

## 🎯 Use Cases

### 1. Real-time Emotion Monitoring
```bash
python live_recorder.py --continuous --duration 3
```
Monitor emotions every 3 seconds

### 2. Voice Diary
```bash
python live_recorder.py --duration 30
```
Record longer thoughts and analyze

### 3. Quick Check
```bash
python live_recorder.py --duration 2 --no-save
```
Quick emotion check without saving

### 4. Testing Different Emotions
```bash
# Record happy voice
python live_recorder.py --duration 5

# Record sad voice
python live_recorder.py --duration 5

# Compare results
```

---

## 📁 Saved Recordings

Recordings are saved to:
```
recordings/
├── recording_20260330_160000.wav
├── recording_20260330_160010.wav
└── recording_20260330_160020.wav
```

Format: `recording_YYYYMMDD_HHMMSS.wav`

---

## 🔧 Troubleshooting

### "Microphone access denied"

**Web App**:
- Click the lock icon in browser address bar
- Allow microphone access
- Refresh page

**Command Line**:
- Check microphone is connected
- Run `python live_recorder.py --list-devices`
- Try different device with `--device INDEX`

### "No audio devices found"

```bash
# Linux: Install PortAudio
sudo apt-get install portaudio19-dev

# Mac: Install PortAudio
brew install portaudio

# Then reinstall sounddevice
pip install --upgrade sounddevice
```

### "Recording is silent"

- Check microphone volume in system settings
- Speak closer to microphone
- Try different device with `--device INDEX`
- Test with: `python -m sounddevice`

### "Permission denied"

**Linux**:
```bash
# Add user to audio group
sudo usermod -a -G audio $USER

# Logout and login again
```

---

## 🎓 Tips for Best Results

### Recording Quality
- ✅ Speak clearly and naturally
- ✅ Use good microphone if available
- ✅ Minimize background noise
- ✅ Speak for at least 3 seconds
- ✅ Express emotion clearly

### Duration Guidelines
- **Quick check**: 2-3 seconds
- **Standard**: 5 seconds (default)
- **Detailed**: 10-15 seconds
- **Long form**: 30+ seconds

### Environment
- Quiet room
- Close to microphone
- No background music
- No other speakers

---

## 🚀 Advanced Usage

### Batch Recording

```bash
#!/bin/bash
# Record 5 different emotions

echo "Record HAPPY emotion"
python live_recorder.py --duration 5

echo "Record SAD emotion"
python live_recorder.py --duration 5

echo "Record ANGRY emotion"
python live_recorder.py --duration 5

echo "Record NEUTRAL emotion"
python live_recorder.py --duration 5

echo "Record FEAR emotion"
python live_recorder.py --duration 5
```

### Integration with Other Scripts

```python
from live_recorder import LiveRecorder

# Create recorder
recorder = LiveRecorder()

# Record and analyze
emotion, confidence, scores = recorder.record_and_analyze(
    duration=5,
    save=True
)

print(f"Detected: {emotion} ({confidence*100:.1f}%)")
```

---

## 📊 Output Format

### Terminal Output
```
🎙️  Recording for 5 seconds...
   Speak now!
   ========================================
   Recording... 5/5 seconds
   ========================================
✓ Recording complete!

💾 Saved to: recordings/recording_20260330_160000.wav

🔧 Processing audio...
🔍 Analyzing emotion...

==================================================
🎯 PREDICTION RESULT
==================================================

😊  Detected Emotion: HAPPY
✓  Confidence: 85.32%
   Confidence Level: HIGH ✓✓✓

📊 Confidence Scores:
========================================
1. HAPPY        █████████████████░░░ 85.32%
2. NEUTRAL      ███░░░░░░░░░░░░░░░░░ 10.45%
3. SURPRISE     █░░░░░░░░░░░░░░░░░░░ 4.23%
```

---

## 🎉 Features Summary

**Web App**:
- ✅ Browser-based recording
- ✅ No installation needed
- ✅ Visual interface
- ✅ Cross-platform

**Command Line**:
- ✅ Quick and efficient
- ✅ Scriptable
- ✅ Continuous mode
- ✅ Device selection
- ✅ Auto-save recordings

**Both**:
- ✅ Real-time emotion detection
- ✅ High-quality audio capture
- ✅ Confidence scores
- ✅ Multiple emotion support

---

## 📝 Next Steps

1. **Try it now**:
   ```bash
   python live_recorder.py
   ```

2. **Test web recording**:
   - Start web app
   - Click record button
   - Analyze results

3. **Experiment**:
   - Try different emotions
   - Test various durations
   - Use continuous mode

---

**🎤 Start recording and detecting emotions in real-time!**
