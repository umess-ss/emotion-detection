"""
Create sample audio files for testing
Run: python create_sample_audio.py
"""

import numpy as np
import soundfile as sf
from pathlib import Path

def create_sample_audio():
    """Create a simple test audio file"""
    
    # Create directory
    Path("sample_audio").mkdir(exist_ok=True)
    
    # Parameters
    sample_rate = 16000
    duration = 3.0
    
    # Generate a simple tone with variation
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Create a more complex waveform
    frequency1 = 440.0  # A note
    frequency2 = 554.37  # C# note
    
    waveform = (
        0.3 * np.sin(2 * np.pi * frequency1 * t) +
        0.2 * np.sin(2 * np.pi * frequency2 * t)
    )
    
    # Add amplitude modulation
    modulation = 0.5 + 0.5 * np.sin(2 * np.pi * 2 * t)
    waveform = waveform * modulation
    
    # Save
    output_path = "sample_audio/test_sample.wav"
    sf.write(output_path, waveform, sample_rate)
    
    print(f"✓ Created: {output_path}")
    print(f"  Duration: {duration}s")
    print(f"  Sample Rate: {sample_rate}Hz")
    print("\nNote: This is synthetic audio for testing only.")
    print("For accurate results, use real voice recordings.")

if __name__ == "__main__":
    create_sample_audio()
