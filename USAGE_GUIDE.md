# Usage Guide

## Quick Start

### 1. Basic Usage

```bash
python main.py --audio sample_audio/your_audio.wav
```

### 2. With Custom Model

```bash
python main.py --audio your_audio.wav --model "ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition"
```

### 3. With GPU (if available)

```bash
python main.py --audio your_audio.wav --gpu
```

### 4. Show System Info

```bash
python main.py --audio your_audio.wav --info
```

## Testing the System

### Run Built-in Tests

```bash
python test_detector.py
```

This will:
- Create a synthetic test audio
- Test all components
- Run a complete prediction
- Show system information

### Test with Your Audio

```bash
python test_detector.py --audio your_recording.wav
```

## Recording Your Own Audio

### Using Audacity (Free, Cross-platform)

1. Download Audacity: https://www.audacityteam.org/
2. Click red record button
3. Speak clearly for 3-10 seconds
4. File → Export → Export as WAV
5. Save to `sample_audio/` folder

### Using Phone

1. Use voice recorder app
2. Record 3-10 seconds
3. Transfer to computer
4. Convert to .wav if needed (use online converter)

### Tips for Best Results

- Speak clearly and naturally
- 3-10 seconds duration is ideal
- Minimize background noise
- Express emotion clearly
- Use good microphone if possible

## Understanding Output

### Example Output

```
🎯 PREDICTION RESULT
==================================================

😊  Detected Emotion: HAPPY
✓  Confidence: 78.45%
   Confidence Level: HIGH ✓✓✓

📊 Confidence Scores:
========================================
1. HAPPY        ████████████████░░░░ 78.45%
2. NEUTRAL      ████░░░░░░░░░░░░░░░░ 12.30%
3. SURPRISE     ██░░░░░░░░░░░░░░░░░░ 5.67%
```

### Interpreting Confidence Levels

- **HIGH (>70%)**: Very confident, reliable prediction
- **MEDIUM (40-70%)**: Moderate confidence, likely correct
- **LOW (<40%)**: Uncertain, may be mixed emotions or unclear audio

