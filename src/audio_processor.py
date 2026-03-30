"""
Audio preprocessing module
Handles loading and preprocessing audio files for emotion detection
"""

import librosa
import numpy as np
import soundfile as sf
from typing import Tuple, Optional
import warnings

warnings.filterwarnings('ignore')


class AudioProcessor:
    """
    Handles all audio preprocessing operations
    """
    
    def __init__(self, target_sample_rate: int = 16000):
        """
        Initialize the audio processor
        
        Args:
            target_sample_rate: Target sampling rate for the model (16kHz is standard)
        """
        self.target_sample_rate = target_sample_rate
        
    def load_audio(self, file_path: str) -> Tuple[np.ndarray, int]:
        """
        Load audio file and return waveform and sample rate
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Tuple of (waveform, sample_rate)
            
        Raises:
            Exception: If audio file cannot be loaded
        """
        try:
            # Load audio file using librosa
            # librosa automatically converts to mono and resamples
            waveform, sample_rate = librosa.load(
                file_path,
                sr=self.target_sample_rate,  # Resample to target rate
                mono=True  # Convert to mono if stereo
            )
            
            print(f"✓ Audio loaded successfully")
            print(f"  - Duration: {len(waveform)/sample_rate:.2f} seconds")
            print(f"  - Sample Rate: {sample_rate} Hz")
            print(f"  - Samples: {len(waveform)}")
            
            return waveform, sample_rate
            
        except Exception as e:
            raise Exception(f"Failed to load audio: {str(e)}")
    
    def preprocess_audio(self, waveform: np.ndarray, sample_rate: int) -> np.ndarray:
        """
        Preprocess audio waveform for model input
        
        Args:
            waveform: Audio waveform as numpy array
            sample_rate: Sample rate of the audio
            
        Returns:
            Preprocessed waveform
        """
        # Ensure correct sample rate
        if sample_rate != self.target_sample_rate:
            waveform = librosa.resample(
                waveform,
                orig_sr=sample_rate,
                target_sr=self.target_sample_rate
            )
        
        # Normalize audio to [-1, 1] range
        if waveform.max() > 1.0 or waveform.min() < -1.0:
            waveform = waveform / np.max(np.abs(waveform))
        
        # Remove silence from beginning and end
        waveform = self._trim_silence(waveform)
        
        print(f"✓ Audio preprocessed")
        
        return waveform
    
    def _trim_silence(self, waveform: np.ndarray, threshold: float = 0.01) -> np.ndarray:
        """
        Remove silence from the beginning and end of audio
        
        Args:
            waveform: Audio waveform
            threshold: Amplitude threshold for silence detection
            
        Returns:
            Trimmed waveform
        """
        # Find non-silent regions
        non_silent = np.abs(waveform) > threshold
        
        if not non_silent.any():
            # If entire audio is silent, return as is
            return waveform
        
        # Find first and last non-silent sample
        first_sound = np.argmax(non_silent)
        last_sound = len(non_silent) - np.argmax(non_silent[::-1]) - 1
        
        return waveform[first_sound:last_sound+1]
    
    def get_audio_features(self, waveform: np.ndarray, sample_rate: int) -> dict:
        """
        Extract basic audio features for analysis (optional, for debugging)
        
        Args:
            waveform: Audio waveform
            sample_rate: Sample rate
            
        Returns:
            Dictionary of audio features
        """
        features = {}
        
        # Duration
        features['duration'] = len(waveform) / sample_rate
        
        # Zero crossing rate (indicates pitch/frequency changes)
        features['zero_crossing_rate'] = np.mean(librosa.zero_crossings(waveform))
        
        # RMS energy (indicates loudness)
        features['rms_energy'] = np.sqrt(np.mean(waveform**2))
        
        # Spectral centroid (indicates brightness of sound)
        spectral_centroids = librosa.feature.spectral_centroid(
            y=waveform, 
            sr=sample_rate
        )[0]
        features['spectral_centroid_mean'] = np.mean(spectral_centroids)
        
        return features
    
    def validate_audio_quality(self, waveform: np.ndarray) -> Tuple[bool, str]:
        """
        Check if audio quality is sufficient for emotion detection
        
        Args:
            waveform: Audio waveform
            
        Returns:
            Tuple of (is_valid, message)
        """
        # Check if audio is too short
        min_duration = 0.5  # seconds
        duration = len(waveform) / self.target_sample_rate
        
        if duration < min_duration:
            return False, f"Audio too short ({duration:.2f}s). Minimum: {min_duration}s"
        
        # Check if audio is too quiet
        rms = np.sqrt(np.mean(waveform**2))
        if rms < 0.001:
            return False, "Audio too quiet. Please use a clearer recording."
        
        # Check if audio is clipped (too loud)
        if np.max(np.abs(waveform)) > 0.99:
            return True, "⚠️  Warning: Audio may be clipped (too loud)"
        
        return True, "Audio quality is good"
