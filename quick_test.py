"""
Quick test with a lighter model
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

print("🧪 Quick Test - Voice Emotion Detection\n")

# Test imports
print("1. Testing imports...")
try:
    import torch
    import transformers
    import librosa
    import soundfile as sf
    import numpy as np
    print("   ✓ All imports successful\n")
except ImportError as e:
    print(f"   ✗ Import failed: {e}")
    sys.exit(1)

# Test audio creation
print("2. Creating test audio...")
try:
    sample_rate = 16000
    duration = 3.0
    t = np.linspace(0, duration, int(sample_rate * duration))
    waveform = 0.3 * np.sin(2 * np.pi * 440 * t)
    
    Path("sample_audio").mkdir(exist_ok=True)
    sf.write("sample_audio/quick_test.wav", waveform, sample_rate)
    print("   ✓ Test audio created\n")
except Exception as e:
    print(f"   ✗ Failed: {e}")
    sys.exit(1)

# Test audio loading
print("3. Testing audio loading...")
try:
    from src.audio_processor import AudioProcessor
    processor = AudioProcessor()
    waveform, sr = processor.load_audio("sample_audio/quick_test.wav")
    print("   ✓ Audio loaded successfully\n")
except Exception as e:
    print(f"   ✗ Failed: {e}")
    sys.exit(1)

# Test preprocessing
print("4. Testing preprocessing...")
try:
    waveform = processor.preprocess_audio(waveform, sr)
    print("   ✓ Preprocessing successful\n")
except Exception as e:
    print(f"   ✗ Failed: {e}")
    sys.exit(1)

print("="*50)
print("✅ ALL BASIC TESTS PASSED!")
print("="*50)
print("\nNote: Model download test skipped for speed.")
print("To test with actual model, run: python test_detector.py")
print("\nYour system is ready for emotion detection!")
