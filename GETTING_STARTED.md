# Getting Started - Complete Beginner's Guide

## Welcome! 👋

This guide will walk you through everything from installation to running your first emotion detection.

## Prerequisites

### What You Need
1. **Computer**: Windows, Mac, or Linux
2. **Python**: Version 3.8 or higher
3. **Internet**: For downloading models (first time only)
4. **RAM**: At least 4GB available
5. **Disk Space**: 2-3GB free

### Check Python Installation

Open terminal/command prompt and run:
```bash
python --version
```

You should see something like `Python 3.9.x` or higher.

If not installed, download from: https://www.python.org/downloads/

## Step-by-Step Installation

### Step 1: Download the Project

Download and extract the project to a folder, for example:
- Windows: `C:\Users\YourName\voice-emotion-detection`
- Mac/Linux: `~/voice-emotion-detection`

### Step 2: Open Terminal

**Windows:**
- Press `Win + R`
- Type `cmd` and press Enter
- Navigate to project: `cd C:\Users\YourName\voice-emotion-detection`

**Mac:**
- Press `Cmd + Space`
- Type `terminal` and press Enter
- Navigate to project: `cd ~/voice-emotion-detection`

**Linux:**
- Open terminal (usually `Ctrl + Alt + T`)
- Navigate to project: `cd ~/voice-emotion-detection`

### Step 3: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

You should see `(venv)` at the start of your command line.

### Step 4: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

This will take 2-5 minutes. You'll see packages being downloaded and installed.

### Step 5: Verify Installation

```bash
python -c "import torch; import transformers; import librosa; print('Success!')"
```

If you see "Success!", you're ready to go!

## Your First Emotion Detection

### Option 1: Use Test Script (Easiest)

```bash
python test_detector.py
```

This will:
1. Create a test audio file
2. Load the model (takes 1-2 minutes first time)
3. Analyze the audio
4. Show results

### Option 2: Use Your Own Audio

#### Record Audio

**Using Phone:**
1. Open voice recorder app
2. Record yourself saying something emotional (3-10 seconds)
3. Transfer file to computer
4. Place in `sample_audio/` folder

**Using Audacity (Free Software):**
1. Download from: https://www.audacityteam.org/
2. Click red record button
3. Speak for 3-10 seconds
4. File → Export → Export as WAV
5. Save to `sample_audio/my_recording.wav`

#### Run Detection

```bash
python main.py --audio sample_audio/my_recording.wav
```

### Option 3: Use GUI

```bash
python gui_simple.py
```

Click "Select Audio File" and choose your audio.

## Understanding the Output

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

### What It Means

- **Detected Emotion**: The most likely emotion
- **Confidence**: How sure the model is (0-100%)
- **Confidence Level**: 
  - HIGH (>70%): Very reliable
  - MEDIUM (40-70%): Probably correct
  - LOW (<40%): Uncertain
- **Top 3 Predictions**: Other possible emotions

## Common First-Time Issues

### Issue: "python: command not found"
**Solution**: Try `python3` instead of `python`

### Issue: "No module named 'torch'"
**Solution**: Run `pip install -r requirements.txt` again

### Issue: Model download is slow
**Solution**: Be patient, it's ~300MB. Only happens once.

### Issue: "Out of memory"
**Solution**: Close other applications, or use lighter model (see TROUBLESHOOTING.md)

### Issue: Low confidence scores
**Solution**: Use clearer audio with less background noise

## Tips for Best Results

### Audio Quality
✅ Clear speech
✅ Minimal background noise
✅ 3-10 seconds duration
✅ Express emotion clearly
✅ Use good microphone

❌ Avoid:
- Very short clips (<1 second)
- Noisy environments
- Mumbling or unclear speech
- Multiple speakers talking

### Recording Tips
1. Find a quiet place
2. Speak clearly and naturally
3. Express the emotion you want to test
4. Keep it 3-10 seconds
5. Save as .wav format

## What to Do Next

### For Learning
1. ✅ Run test_detector.py
2. ✅ Try with your own audio
3. ✅ Read ARCHITECTURE.md to understand how it works
4. ✅ Explore the code in `src/` folder
5. ✅ Try different models (see MODEL_COMPARISON.md)

### For Projects
1. ✅ Customize the code
2. ✅ Add new features (see IMPROVEMENTS.md)
3. ✅ Create a GUI (gui_simple.py is a start)
4. ✅ Deploy as web app (see DEPLOYMENT.md)
5. ✅ Add to your portfolio

### For Interviews
1. ✅ Read VIVA_QUESTIONS.md
2. ✅ Understand the architecture
3. ✅ Practice explaining the project
4. ✅ Prepare demo
5. ✅ Use RESUME_DESCRIPTION.md for portfolio

## Project Structure Explained

```
voice-emotion-detection/
├── src/                      # Core code
│   ├── emotion_detector.py   # ML model logic
│   ├── audio_processor.py    # Audio handling
│   └── utils.py              # Helper functions
├── sample_audio/             # Your audio files go here
├── main.py                   # Run this for CLI
├── gui_simple.py             # Run this for GUI
├── test_detector.py          # Run this to test
└── requirements.txt          # Dependencies list
```

## Quick Commands Reference

```bash
# Test the system
python test_detector.py

# Analyze audio (CLI)
python main.py --audio sample_audio/test.wav

# Launch GUI
python gui_simple.py

# Use GPU (if available)
python main.py --audio test.wav --gpu

# Get help
python main.py --help
```

## Learning Resources

### Understanding the Code
- Start with `main.py` - entry point
- Then `emotion_detector.py` - core logic
- Then `audio_processor.py` - audio handling
- Finally `utils.py` - helpers

### Understanding the Concepts
- Read ARCHITECTURE.md for technical details
- Check MODEL_COMPARISON.md for model info
- See VIVA_QUESTIONS.md for Q&A

### Improving the Project
- IMPROVEMENTS.md for ideas
- DEPLOYMENT.md for deployment
- TROUBLESHOOTING.md for issues

## Getting Help

### Documentation
1. QUICK_REFERENCE.md - Quick answers
2. TROUBLESHOOTING.md - Fix problems
3. VIVA_QUESTIONS.md - Understand concepts

### Online Resources
- Hugging Face Docs: https://huggingface.co/docs
- PyTorch Tutorials: https://pytorch.org/tutorials
- librosa Docs: https://librosa.org/doc

### Community
- Stack Overflow: Tag with `python`, `pytorch`, `huggingface`
- Hugging Face Forums: https://discuss.huggingface.co
- Reddit: r/MachineLearning, r/learnpython

## Success Checklist

After following this guide, you should be able to:
- [ ] Install all dependencies
- [ ] Run test_detector.py successfully
- [ ] Analyze your own audio file
- [ ] Understand the output
- [ ] Explain what the system does
- [ ] Navigate the code structure

## Congratulations! 🎉

You've successfully set up and run your first emotion detection system!

### Next Steps
1. Try different audio samples
2. Experiment with the code
3. Read the architecture documentation
4. Add your own improvements
5. Deploy it somewhere
6. Add to your portfolio

### Questions?
- Check TROUBLESHOOTING.md
- Read VIVA_QUESTIONS.md
- Search online
- Ask in forums

**Happy coding!** 🚀
