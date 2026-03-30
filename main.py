"""
Main entry point for Voice Emotion Detection System
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.emotion_detector import EmotionDetector
from src.audio_processor import AudioProcessor
from src.utils import (
    validate_audio_file,
    print_header,
    print_result,
    check_dependencies,
    print_system_info
)


def main():
    """Main function to run emotion detection"""
    
    # Print header
    print_header()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Detect emotions from voice recordings'
    )
    parser.add_argument(
        '--audio',
        type=str,
        required=True,
        help='Path to audio file (.wav, .mp3, .flac, .ogg)'
    )
    parser.add_argument(
        '--model',
        type=str,
        default=None,
        help='Hugging Face model name (optional)'
    )
    parser.add_argument(
        '--gpu',
        action='store_true',
        help='Use GPU if available'
    )
    parser.add_argument(
        '--info',
        action='store_true',
        help='Show system information'
    )
    
    args = parser.parse_args()
    
    # Show system info if requested
    if args.info:
        print_system_info()
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    all_installed, missing = check_dependencies()
    
    if not all_installed:
        print(f"\n❌ Missing dependencies: {', '.join(missing)}")
        print("Please run: pip install -r requirements.txt")
        sys.exit(1)
    
    print("✓ All dependencies installed\n")
    
    # Validate audio file
    print(f"📁 Validating audio file: {args.audio}")
    is_valid, message = validate_audio_file(args.audio)
    
    if not is_valid:
        print(f"❌ {message}")
        sys.exit(1)
    
    print(f"✓ {message}\n")
    
    try:
        # Initialize audio processor
        print("🎵 Initializing audio processor...")
        audio_processor = AudioProcessor(target_sample_rate=16000)
        
        # Load audio
        print(f"📂 Loading audio file...")
        waveform, sample_rate = audio_processor.load_audio(args.audio)
        
        # Validate audio quality
        is_valid, quality_msg = audio_processor.validate_audio_quality(waveform)
        print(f"   {quality_msg}")
        
        if not is_valid:
            print(f"❌ Audio quality check failed")
            sys.exit(1)
        
        # Preprocess audio
        print("\n🔧 Preprocessing audio...")
        waveform = audio_processor.preprocess_audio(waveform, sample_rate)
        
        # Initialize emotion detector
        print("\n🤖 Initializing emotion detector...")
        detector = EmotionDetector(
            model_name=args.model,
            use_gpu=args.gpu
        )
        
        # Show model info
        model_info = detector.get_model_info()
        print(f"📊 Model Info:")
        print(f"   - Emotions: {', '.join(model_info['emotions'])}")
        print(f"   - Device: {model_info['device']}")
        
        # Predict emotion
        emotion, confidence, all_scores = detector.predict(waveform, sample_rate)
        
        # Print results
        print_result(emotion, confidence, all_scores)
        
        # Interpretation tips
        print("💡 Tips:")
        if confidence < 0.4:
            print("   - Low confidence may indicate unclear speech or mixed emotions")
            print("   - Try using a clearer recording with less background noise")
        
        print("   - For best results, use 3-10 second audio clips")
        print("   - Ensure the speaker's voice is clear and prominent")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user")
        sys.exit(0)
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Ensure audio file is not corrupted")
        print("2. Check if you have enough RAM (4GB minimum)")
        print("3. Try with a shorter audio clip")
        print("4. Check internet connection (first run downloads model)")
        sys.exit(1)


if __name__ == "__main__":
    main()
