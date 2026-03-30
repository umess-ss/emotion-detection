"""
Test script for Voice Emotion Detection System
Creates a synthetic audio file for testing if no sample is available
"""

import sys
import numpy as np
import soundfile as sf
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.emotion_detector import EmotionDetector
from src.audio_processor import AudioProcessor
from src.utils import print_header, print_result


def create_test_audio(output_path: str = "sample_audio/test_tone.wav"):
    """
    Create a simple test audio file (sine wave)
    
    Args:
        output_path: Where to save the test audio
    """
    print("🔧 Creating test audio file...")
    
    # Create directory if it doesn't exist
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Generate a 3-second sine wave at 440 Hz (A note)
    sample_rate = 16000
    duration = 3.0
    frequency = 440.0
    
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Create sine wave with some variation (to simulate speech-like patterns)
    waveform = np.sin(2 * np.pi * frequency * t)
    
    # Add some amplitude modulation (to make it more interesting)
    modulation = 0.5 + 0.5 * np.sin(2 * np.pi * 2 * t)
    waveform = waveform * modulation
    
    # Normalize
    waveform = waveform * 0.3
    
    # Save as WAV file
    sf.write(output_path, waveform, sample_rate)
    
    print(f"✓ Test audio created: {output_path}")
    print(f"  Note: This is a synthetic tone, not real speech.")
    print(f"  For accurate testing, use real voice recordings.\n")
    
    return output_path


def test_basic_functionality():
    """Test basic emotion detection functionality"""
    
    print_header()
    print("🧪 Running Basic Functionality Tests\n")
    print("="*50)
    
    try:
        # Test 1: Check imports
        print("\n✓ Test 1: Imports successful")
        
        # Test 2: Initialize audio processor
        print("✓ Test 2: Audio processor initialized")
        audio_processor = AudioProcessor()
        
        # Test 3: Create test audio
        test_audio_path = create_test_audio()
        
        # Test 4: Load audio
        print("🔄 Test 3: Loading test audio...")
        waveform, sample_rate = audio_processor.load_audio(test_audio_path)
        print("✓ Test 3: Audio loaded successfully")
        
        # Test 5: Preprocess audio
        print("\n🔄 Test 4: Preprocessing audio...")
        waveform = audio_processor.preprocess_audio(waveform, sample_rate)
        print("✓ Test 4: Audio preprocessed successfully")
        
        # Test 6: Initialize detector
        print("\n🔄 Test 5: Initializing emotion detector...")
        print("   (This will download the model on first run - may take a few minutes)")
        detector = EmotionDetector(use_gpu=False)
        print("✓ Test 5: Detector initialized successfully")
        
        # Test 7: Run prediction
        print("\n🔄 Test 6: Running emotion prediction...")
        emotion, confidence, all_scores = detector.predict(waveform, sample_rate)
        print("✓ Test 6: Prediction completed successfully")
        
        # Display results
        print_result(emotion, confidence, all_scores)
        
        # Test 8: Model info
        print("🔄 Test 7: Getting model information...")
        model_info = detector.get_model_info()
        print("✓ Test 7: Model info retrieved")
        print(f"\n📊 Model Information:")
        for key, value in model_info.items():
            print(f"   {key}: {value}")
        
        print("\n" + "="*50)
        print("✅ ALL TESTS PASSED!")
        print("="*50)
        
        print("\n💡 Next Steps:")
        print("1. Test with your own voice recording:")
        print("   python main.py --audio your_audio.wav")
        print("\n2. Record a voice sample using your phone or computer")
        print("   - Say a sentence with clear emotion (happy, sad, angry, etc.)")
        print("   - Save as .wav format")
        print("   - Place in sample_audio/ folder")
        print("\n3. Run the detector on your recording")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Ensure all dependencies are installed:")
        print("   pip install -r requirements.txt")
        print("\n2. Check internet connection (needed for first run)")
        print("\n3. Ensure you have at least 4GB RAM available")
        sys.exit(1)


def test_with_custom_audio(audio_path: str):
    """
    Test with a custom audio file
    
    Args:
        audio_path: Path to audio file
    """
    print_header()
    print(f"🧪 Testing with custom audio: {audio_path}\n")
    
    try:
        # Initialize components
        audio_processor = AudioProcessor()
        detector = EmotionDetector(use_gpu=False)
        
        # Process audio
        waveform, sample_rate = audio_processor.load_audio(audio_path)
        waveform = audio_processor.preprocess_audio(waveform, sample_rate)
        
        # Predict
        emotion, confidence, all_scores = detector.predict(waveform, sample_rate)
        
        # Show results
        print_result(emotion, confidence, all_scores)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Test emotion detection system')
    parser.add_argument(
        '--audio',
        type=str,
        default=None,
        help='Path to custom audio file for testing'
    )
    
    args = parser.parse_args()
    
    if args.audio:
        test_with_custom_audio(args.audio)
    else:
        test_basic_functionality()
