"""
Utility functions for the Voice Emotion Detection system
"""

import os
import sys
from typing import Dict, List, Tuple


def validate_audio_file(file_path: str) -> Tuple[bool, str]:
    """
    Validate if the audio file exists and has correct format
    
    Args:
        file_path: Path to the audio file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check if file exists
    if not os.path.exists(file_path):
        return False, f"File not found: {file_path}"
    
    # Check file extension
    valid_extensions = ['.wav', '.mp3', '.flac', '.ogg']
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext not in valid_extensions:
        return False, f"Unsupported format: {file_ext}. Supported: {', '.join(valid_extensions)}"
    
    # Check file size (warn if too large)
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb > 50:
        print(f"⚠️  Warning: Large file ({file_size_mb:.1f}MB). Processing may be slow.")
    
    return True, "Valid audio file"


def format_confidence_scores(scores: Dict[str, float], top_n: int = 3) -> str:
    """
    Format confidence scores for display
    
    Args:
        scores: Dictionary of emotion -> confidence score
        top_n: Number of top predictions to show
        
    Returns:
        Formatted string with top predictions
    """
    # Sort by confidence (highest first)
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    output = "\n📊 Confidence Scores:\n"
    output += "=" * 40 + "\n"
    
    for i, (emotion, score) in enumerate(sorted_scores[:top_n], 1):
        # Create a simple progress bar
        bar_length = int(score * 20)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        
        output += f"{i}. {emotion.upper():12} {bar} {score*100:.2f}%\n"
    
    return output


def print_header():
    """Print a nice header for the application"""
    header = """
    ╔═══════════════════════════════════════════════╗
    ║   🎤 Voice Emotion Detection System 🎭       ║
    ║   Powered by Hugging Face Transformers       ║
    ╚═══════════════════════════════════════════════╝
    """
    print(header)


def print_result(emotion: str, confidence: float, all_scores: Dict[str, float]):
    """
    Print the detection result in a nice format
    
    Args:
        emotion: Predicted emotion
        confidence: Confidence score for the prediction
        all_scores: All emotion scores
    """
    print("\n" + "="*50)
    print("🎯 PREDICTION RESULT")
    print("="*50)
    
    # Emotion emoji mapping
    emoji_map = {
        'happy': '😊',
        'sad': '😢',
        'angry': '😠',
        'neutral': '😐',
        'fear': '😨',
        'disgust': '🤢',
        'surprise': '😲'
    }
    
    emoji = emoji_map.get(emotion.lower(), '🎭')
    
    print(f"\n{emoji}  Detected Emotion: {emotion.upper()}")
    print(f"✓  Confidence: {confidence*100:.2f}%")
    
    # Show confidence level
    if confidence > 0.7:
        print("   Confidence Level: HIGH ✓✓✓")
    elif confidence > 0.4:
        print("   Confidence Level: MEDIUM ✓✓")
    else:
        print("   Confidence Level: LOW ✓")
    
    # Show all scores
    print(format_confidence_scores(all_scores))
    print("="*50 + "\n")


def check_dependencies() -> Tuple[bool, List[str]]:
    """
    Check if all required dependencies are installed
    
    Returns:
        Tuple of (all_installed, missing_packages)
    """
    required_packages = [
        'torch',
        'transformers',
        'librosa',
        'soundfile',
        'numpy'
    ]
    
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    return len(missing) == 0, missing


def print_system_info():
    """Print system information for debugging"""
    import platform
    
    print("\n📋 System Information:")
    print(f"   Python Version: {sys.version.split()[0]}")
    print(f"   Platform: {platform.system()} {platform.release()}")
    
    try:
        import torch
        print(f"   PyTorch Version: {torch.__version__}")
        print(f"   CUDA Available: {torch.cuda.is_available()}")
    except ImportError:
        print("   PyTorch: Not installed")
    
    print()
