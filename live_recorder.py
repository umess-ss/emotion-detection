"""
Live Voice Recording and Emotion Detection
Records audio from microphone and detects emotion in real-time
"""

import sys
from pathlib import Path
import numpy as np
import sounddevice as sd
import soundfile as sf
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from src.emotion_detector import EmotionDetector
from src.audio_processor import AudioProcessor
from src.utils import print_header, print_result

class LiveRecorder:
    """Record and analyze live audio"""
    
    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate
        self.processor = AudioProcessor(target_sample_rate=sample_rate)
        self.detector = None
        
    def list_devices(self):
        """List available audio input devices"""
        print("\n🎤 Available Audio Devices:\n")
        devices = sd.query_devices()
        for i, device in enumerate(devices):
            if device['max_input_channels'] > 0:
                print(f"  [{i}] {device['name']}")
                print(f"      Channels: {device['max_input_channels']}")
                print(f"      Sample Rate: {device['default_samplerate']}")
                print()
    
    def record(self, duration=5, device=None):
        """
        Record audio from microphone
        
        Args:
            duration: Recording duration in seconds
            device: Device index (None for default)
            
        Returns:
            Audio waveform as numpy array
        """
        print(f"\n🎙️  Recording for {duration} seconds...")
        print("   Speak now!")
        print("   " + "="*40)
        
        # Record audio
        recording = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            device=device,
            dtype='float32'
        )
        
        # Show progress
        for i in range(duration):
            print(f"   Recording... {i+1}/{duration} seconds", end='\r')
            sd.wait(int(self.sample_rate))
        
        print("\n   " + "="*40)
        print("✓ Recording complete!\n")
        
        # Wait for recording to finish
        sd.wait()
        
        return recording.flatten()
    
    def save_recording(self, waveform, filename=None):
        """Save recording to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recordings/recording_{timestamp}.wav"
        
        # Create directory
        Path(filename).parent.mkdir(exist_ok=True)
        
        # Save
        sf.write(filename, waveform, self.sample_rate)
        print(f"💾 Saved to: {filename}\n")
        
        return filename
    
    def analyze(self, waveform):
        """Analyze recorded audio"""
        # Initialize detector if needed
        if self.detector is None:
            print("🤖 Loading emotion detection model...")
            self.detector = EmotionDetector()
            print()
        
        # Preprocess
        print("🔧 Processing audio...")
        waveform = self.processor.preprocess_audio(waveform, self.sample_rate)
        
        # Validate
        is_valid, msg = self.processor.validate_audio_quality(waveform)
        if not is_valid:
            print(f"⚠️  Warning: {msg}")
            return None, None, None
        
        # Predict
        print("🔍 Analyzing emotion...\n")
        emotion, confidence, all_scores = self.detector.predict(
            waveform, 
            self.sample_rate
        )
        
        return emotion, confidence, all_scores
    
    def record_and_analyze(self, duration=5, device=None, save=True):
        """Record and analyze in one go"""
        # Record
        waveform = self.record(duration, device)
        
        # Save if requested
        if save:
            self.save_recording(waveform)
        
        # Analyze
        emotion, confidence, all_scores = self.analyze(waveform)
        
        if emotion:
            print_result(emotion, confidence, all_scores)
        
        return emotion, confidence, all_scores


def main():
    """Main function for live recording"""
    import argparse
    
    print_header()
    
    parser = argparse.ArgumentParser(
        description='Record live audio and detect emotions'
    )
    parser.add_argument(
        '--duration',
        type=int,
        default=5,
        help='Recording duration in seconds (default: 5)'
    )
    parser.add_argument(
        '--device',
        type=int,
        default=None,
        help='Audio input device index'
    )
    parser.add_argument(
        '--list-devices',
        action='store_true',
        help='List available audio devices'
    )
    parser.add_argument(
        '--no-save',
        action='store_true',
        help='Do not save recording to file'
    )
    parser.add_argument(
        '--continuous',
        action='store_true',
        help='Continuous recording mode'
    )
    
    args = parser.parse_args()
    
    # Create recorder
    recorder = LiveRecorder()
    
    # List devices if requested
    if args.list_devices:
        recorder.list_devices()
        return
    
    try:
        if args.continuous:
            print("🔄 Continuous recording mode")
            print("   Press Ctrl+C to stop\n")
            
            count = 1
            while True:
                print(f"\n{'='*50}")
                print(f"Recording #{count}")
                print('='*50)
                
                recorder.record_and_analyze(
                    duration=args.duration,
                    device=args.device,
                    save=not args.no_save
                )
                
                count += 1
                print("\n⏸️  Press Ctrl+C to stop, or wait for next recording...")
                import time
                time.sleep(2)
        else:
            # Single recording
            recorder.record_and_analyze(
                duration=args.duration,
                device=args.device,
                save=not args.no_save
            )
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Recording stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check if microphone is connected")
        print("2. Run with --list-devices to see available devices")
        print("3. Try specifying device with --device <index>")
        sys.exit(1)


if __name__ == "__main__":
    main()
