# Project Architecture

## System Overview

The Voice Emotion Detection system follows a modular architecture with clear separation of concerns:

```
User Audio Input → Audio Processing → Feature Extraction → Model Inference → Emotion Prediction
```

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        USER INPUT                            │
│                    (Audio File: .wav)                        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   AUDIO PROCESSOR                            │
│  ┌────────────────────────────────────────────────────┐    │
│  │ 1. Load Audio (librosa)                            │    │
│  │ 2. Resample to 16kHz                               │    │
│  │ 3. Convert to Mono                                 │    │
│  │ 4. Normalize Amplitude                             │    │
│  │ 5. Trim Silence                                    │    │
│  │ 6. Validate Quality                                │    │
│  └────────────────────────────────────────────────────┘    │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              FEATURE EXTRACTOR (HuBERT)                      │
│  ┌────────────────────────────────────────────────────┐    │
│  │ 1. Convert waveform to features                    │    │
│  │ 2. Apply model-specific preprocessing              │    │
│  │ 3. Create input tensors                            │    │
│  └────────────────────────────────────────────────────┘    │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│           EMOTION DETECTION MODEL                            │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Pre-trained HuBERT Model                           │    │
│  │ - 24 transformer layers                            │    │
│  │ - Self-attention mechanism                         │    │
│  │ - Fine-tuned on emotion datasets                   │    │
│  │                                                     │    │
│  │ Input: Audio features                              │    │
│  │ Output: Logits for 7 emotions                      │    │
│  └────────────────────────────────────────────────────┘    │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                POST-PROCESSING                               │
│  ┌────────────────────────────────────────────────────┐    │
│  │ 1. Apply Softmax to logits                         │    │
│  │ 2. Get probabilities for each emotion              │    │
│  │ 3. Select highest probability                      │    │
│  │ 4. Format results                                  │    │
│  └────────────────────────────────────────────────────┘    │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    OUTPUT                                    │
│  - Predicted Emotion (happy, sad, angry, etc.)              │
│  - Confidence Score (0-100%)                                │
│  - All Emotion Probabilities                                │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Audio Processor (`audio_processor.py`)
- Handles all audio I/O and preprocessing
- Uses librosa for audio manipulation
- Ensures consistent format for model input

Key Functions:
- `load_audio()`: Load and resample audio
- `preprocess_audio()`: Normalize and clean audio
- `validate_audio_quality()`: Check if audio is suitable

### 2. Emotion Detector (`emotion_detector.py`)
- Manages the ML model
- Handles inference and prediction
- Converts model outputs to human-readable results

Key Functions:
- `__init__()`: Load pre-trained model
- `predict()`: Run emotion detection
- `_get_all_scores()`: Get confidence for all emotions

### 3. Utilities (`utils.py`)
- Helper functions for validation and display
- Error handling and user feedback
- System checks

### 4. Main Entry Point (`main.py`)
- Command-line interface
- Orchestrates the entire pipeline
- Error handling and user guidance

## Data Flow

1. **Input Stage**
   - User provides audio file path
   - System validates file existence and format

2. **Loading Stage**
   - Audio file loaded into memory
   - Converted to numpy array (waveform)
   - Sample rate extracted

3. **Preprocessing Stage**
   - Resampling to 16kHz (model requirement)
   - Mono conversion (if stereo)
   - Amplitude normalization
   - Silence trimming

4. **Feature Extraction Stage**
   - Waveform → Feature Extractor
   - Creates model-compatible input tensors
   - Applies padding if needed

5. **Inference Stage**
   - Features → Pre-trained Model
   - Forward pass through neural network
   - Generates logits (raw scores)

6. **Post-processing Stage**
   - Logits → Softmax → Probabilities
   - Argmax to get predicted class
   - Map class ID to emotion label

7. **Output Stage**
   - Display predicted emotion
   - Show confidence score
   - Present all emotion probabilities

## Model Architecture (HuBERT)

HuBERT (Hidden-Unit BERT) is a self-supervised speech representation model:

```
Audio Waveform
      ↓
CNN Feature Encoder (7 layers)
      ↓
Transformer Encoder (24 layers)
      ↓
Self-Attention Mechanism
      ↓
Contextualized Representations
      ↓
Classification Head
      ↓
7 Emotion Classes
```

Key Features:
- Pre-trained on large speech datasets
- Fine-tuned for emotion recognition
- Captures prosodic and acoustic features
- Robust to noise and variations

## Technology Stack

### Core Libraries
- **PyTorch**: Deep learning framework
- **Transformers**: Hugging Face model library
- **librosa**: Audio processing
- **numpy**: Numerical operations

### Why These Choices?

1. **PyTorch**: Industry standard, great community support
2. **Hugging Face**: Easy access to pre-trained models
3. **librosa**: Comprehensive audio processing toolkit
4. **HuBERT Model**: State-of-the-art for speech tasks

## Performance Considerations

### Memory Usage
- Model size: ~300MB
- Runtime memory: ~2-4GB
- Audio buffer: Depends on file size

### Speed
- Model loading: 5-30 seconds (first time)
- Inference: 1-5 seconds per audio file
- Preprocessing: <1 second

### Optimization Tips
- Use CPU-only PyTorch for smaller footprint
- Process shorter audio clips (<10s)
- Batch processing for multiple files
- Cache model in memory for repeated use

## Error Handling

The system includes comprehensive error handling:

1. **File Validation**: Check existence and format
2. **Dependency Checks**: Verify all libraries installed
3. **Audio Quality**: Validate duration and amplitude
4. **Model Loading**: Handle download failures
5. **Inference Errors**: Catch and explain failures

## Extensibility

The modular design allows easy extensions:

1. **Add New Models**: Modify `MODEL_NAME` in `emotion_detector.py`
2. **Custom Preprocessing**: Extend `AudioProcessor` class
3. **New Output Formats**: Add functions to `utils.py`
4. **Batch Processing**: Use `predict_batch()` method
5. **GUI Integration**: Import classes into GUI code

## Security Considerations

- No external API calls (after model download)
- All processing done locally
- No data sent to external servers
- User audio files never leave the system
