"""
Main emotion detection module using Hugging Face models
"""

import torch
import numpy as np
from transformers import AutoFeatureExtractor, AutoModelForAudioClassification
from typing import Dict, Tuple, Optional
import warnings

warnings.filterwarnings('ignore')


class EmotionDetector:
    """
    Voice Emotion Detection using pre-trained Hugging Face models
    """
    
    # Model configuration
    MODEL_NAME = "superb/hubert-large-superb-er"
    
    # Emotion labels for the model
    # Note: Different models may have different label sets
    EMOTION_LABELS = {
        0: 'neutral',
        1: 'happy',
        2: 'sad',
        3: 'angry',
        4: 'fear',
        5: 'disgust',
        6: 'surprise'
    }
    
    def __init__(self, model_name: Optional[str] = None, use_gpu: bool = False):
        """
        Initialize the emotion detector
        
        Args:
            model_name: Hugging Face model name (uses default if None)
            use_gpu: Whether to use GPU if available
        """
        self.model_name = model_name or self.MODEL_NAME
        self.device = self._setup_device(use_gpu)
        
        print(f"\n🔄 Loading model: {self.model_name}")
        print(f"   Device: {self.device}")
        print("   This may take a few minutes on first run...")
        
        # Load feature extractor and model
        self.feature_extractor = None
        self.model = None
        self._load_model()
        
        print("✓ Model loaded successfully!\n")
    
    def _setup_device(self, use_gpu: bool) -> str:
        """
        Setup computation device (CPU or GPU)
        
        Args:
            use_gpu: Whether to attempt GPU usage
            
        Returns:
            Device string ('cuda' or 'cpu')
        """
        if use_gpu and torch.cuda.is_available():
            return 'cuda'
        else:
            if use_gpu and not torch.cuda.is_available():
                print("⚠️  GPU requested but not available. Using CPU.")
            return 'cpu'
    
    def _load_model(self):
        """
        Load the pre-trained model and feature extractor from Hugging Face
        
        Raises:
            Exception: If model loading fails
        """
        try:
            # Load feature extractor (converts audio to model input format)
            self.feature_extractor = AutoFeatureExtractor.from_pretrained(
                self.model_name
            )
            
            # Load pre-trained model
            self.model = AutoModelForAudioClassification.from_pretrained(
                self.model_name
            )
            
            # Move model to device (CPU or GPU)
            self.model.to(self.device)
            
            # Set model to evaluation mode (disables dropout, etc.)
            self.model.eval()
            
        except Exception as e:
            raise Exception(f"Failed to load model: {str(e)}")
    
    def predict(self, waveform: np.ndarray, sample_rate: int = 16000) -> Tuple[str, float, Dict[str, float]]:
        """
        Predict emotion from audio waveform
        
        Args:
            waveform: Audio waveform as numpy array
            sample_rate: Sample rate of the audio (should be 16000)
            
        Returns:
            Tuple of (predicted_emotion, confidence, all_scores)
        """
        print("🔍 Analyzing emotion...")
        
        try:
            # Preprocess audio using feature extractor
            inputs = self.feature_extractor(
                waveform,
                sampling_rate=sample_rate,
                return_tensors="pt",  # Return PyTorch tensors
                padding=True
            )
            
            # Move inputs to device
            inputs = {key: val.to(self.device) for key, val in inputs.items()}
            
            # Run inference (no gradient calculation needed)
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            # Get logits (raw model outputs)
            logits = outputs.logits
            
            # Convert logits to probabilities using softmax
            probabilities = torch.nn.functional.softmax(logits, dim=-1)
            
            # Get predicted class and confidence
            predicted_class = torch.argmax(probabilities, dim=-1).item()
            confidence = probabilities[0][predicted_class].item()
            
            # Get emotion label
            predicted_emotion = self._get_emotion_label(predicted_class)
            
            # Get all emotion scores
            all_scores = self._get_all_scores(probabilities[0])
            
            print("✓ Analysis complete!\n")
            
            return predicted_emotion, confidence, all_scores
            
        except Exception as e:
            raise Exception(f"Prediction failed: {str(e)}")
    
    def _get_emotion_label(self, class_id: int) -> str:
        """
        Convert class ID to emotion label
        
        Args:
            class_id: Predicted class ID
            
        Returns:
            Emotion label string
        """
        # Try to get label from model config first
        if hasattr(self.model.config, 'id2label'):
            return self.model.config.id2label.get(class_id, 'unknown')
        
        # Fallback to default labels
        return self.EMOTION_LABELS.get(class_id, 'unknown')
    
    def _get_all_scores(self, probabilities: torch.Tensor) -> Dict[str, float]:
        """
        Get confidence scores for all emotions
        
        Args:
            probabilities: Probability tensor from model
            
        Returns:
            Dictionary mapping emotion -> confidence score
        """
        scores = {}
        
        for i in range(len(probabilities)):
            emotion = self._get_emotion_label(i)
            score = probabilities[i].item()
            scores[emotion] = score
        
        return scores
    
    def predict_batch(self, waveforms: list, sample_rate: int = 16000) -> list:
        """
        Predict emotions for multiple audio files (batch processing)
        
        Args:
            waveforms: List of audio waveforms
            sample_rate: Sample rate of the audio
            
        Returns:
            List of (emotion, confidence, all_scores) tuples
        """
        results = []
        
        print(f"🔄 Processing {len(waveforms)} audio files...")
        
        for i, waveform in enumerate(waveforms, 1):
            print(f"\n[{i}/{len(waveforms)}]")
            result = self.predict(waveform, sample_rate)
            results.append(result)
        
        return results
    
    def get_model_info(self) -> Dict[str, any]:
        """
        Get information about the loaded model
        
        Returns:
            Dictionary with model information
        """
        info = {
            'model_name': self.model_name,
            'device': self.device,
            'num_labels': self.model.config.num_labels if hasattr(self.model.config, 'num_labels') else 'unknown',
            'sample_rate': 16000,
            'emotions': list(set(self._get_emotion_label(i) for i in range(7)))
        }
        
        return info
