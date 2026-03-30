# Model Comparison Guide

## Available Models for Emotion Detection

### 1. superb/hubert-large-superb-er (Default)

**Specifications:**
- Size: ~300MB
- Architecture: HuBERT (Hidden-Unit BERT)
- Layers: 24 transformer layers
- Parameters: ~300M
- Training: Pre-trained on LibriSpeech, fine-tuned on emotion data

**Pros:**
- High accuracy
- Robust to noise
- Good generalization
- Well-maintained

**Cons:**
- Larger size
- Slower on CPU
- Requires more RAM

**Best For:**
- Desktop applications
- When accuracy is priority
- Systems with 4GB+ RAM

**Usage:**
```python
MODEL_NAME = "superb/hubert-large-superb-er"
```

---

### 2. ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition

**Specifications:**
- Size: ~1.2GB
- Architecture: Wav2Vec2 XLSR
- Multilingual base
- Fine-tuned for English emotions

**Pros:**
- Very high accuracy
- Multilingual foundation
- Good for diverse accents

**Cons:**
- Large size
- Slower inference
- High memory usage

**Best For:**
- Research projects
- When maximum accuracy needed
- Diverse speaker populations

**Usage:**
```python
MODEL_NAME = "ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition"
```

---

### 3. speechbrain/emotion-recognition-wav2vec2-IEMOCAP

**Specifications:**
- Size: ~400MB
- Architecture: Wav2Vec2
- Trained on IEMOCAP dataset
- 4 emotions: neutral, happy, sad, angry

**Pros:**
- Good balance of size/accuracy
- Fast inference
- Well-documented

**Cons:**
- Only 4 emotions
- Less robust to noise

**Best For:**
- Basic emotion detection
- Faster processing
- Limited resources

**Usage:**
```python
MODEL_NAME = "speechbrain/emotion-recognition-wav2vec2-IEMOCAP"
```

---

### 4. facebook/wav2vec2-base

**Specifications:**
- Size: ~360MB
- Architecture: Wav2Vec2 Base
- Pre-trained only (needs fine-tuning)

**Pros:**
- Good foundation
- Flexible for custom training

**Cons:**
- Not fine-tuned for emotions
- Requires additional training

**Best For:**
- Custom emotion categories
- Research and experimentation
- When you have labeled data

---

### 5. MIT/ast-finetuned-speech-commands-v2

**Specifications:**
- Size: ~340MB
- Architecture: Audio Spectrogram Transformer
- Different approach (spectrogram-based)

**Pros:**
- Novel architecture
- Good for audio classification

**Cons:**
- Not specifically for emotions
- May need adaptation

**Best For:**
- Experimentation
- Comparing architectures

---

## Comparison Table

| Model | Size | Speed | Accuracy | RAM | Emotions | Best Use Case |
|-------|------|-------|----------|-----|----------|---------------|
| HuBERT-large | 300MB | Medium | High | 4GB | 7 | Default choice |
| Wav2Vec2-XLSR | 1.2GB | Slow | Very High | 6GB | 7 | Maximum accuracy |
| SpeechBrain | 400MB | Fast | Good | 3GB | 4 | Limited resources |
| Wav2Vec2-base | 360MB | Medium | N/A | 4GB | Custom | Research |

## Performance Benchmarks

### Inference Time (CPU)
- HuBERT-large: 2-4 seconds
- Wav2Vec2-XLSR: 4-6 seconds
- SpeechBrain: 1-3 seconds

### Memory Usage
- HuBERT-large: 2-4GB
- Wav2Vec2-XLSR: 4-6GB
- SpeechBrain: 2-3GB

### Accuracy (Approximate)
- HuBERT-large: 75-85%
- Wav2Vec2-XLSR: 80-90%
- SpeechBrain: 70-80%

*Note: Accuracy varies by dataset and audio quality*

## How to Switch Models

### Method 1: Edit Code
```python
# In src/emotion_detector.py, line 18
MODEL_NAME = "your-chosen-model"
```

### Method 2: Command Line
```bash
python main.py --audio test.wav --model "speechbrain/emotion-recognition-wav2vec2-IEMOCAP"
```

### Method 3: Programmatic
```python
from src.emotion_detector import EmotionDetector

detector = EmotionDetector(
    model_name="ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition"
)
```

## Choosing the Right Model

### For Students/Learning
✅ **HuBERT-large** (default)
- Good balance
- Well-documented
- Standard choice

### For Low-Resource Systems
✅ **SpeechBrain**
- Smaller size
- Faster inference
- Lower RAM

### For Maximum Accuracy
✅ **Wav2Vec2-XLSR**
- Best performance
- More robust
- Worth the size

### For Custom Emotions
✅ **Wav2Vec2-base** + Fine-tuning
- Flexible
- Trainable
- Research-oriented

## Model Architecture Comparison

### HuBERT (Hidden-Unit BERT)
```
Audio → CNN Encoder → Transformer → Classification
- Self-supervised pre-training
- Masked prediction
- Contextual representations
```

### Wav2Vec2
```
Audio → CNN Encoder → Transformer → Quantization
- Contrastive learning
- Latent representations
- Fine-tuning for downstream tasks
```

### Audio Spectrogram Transformer
```
Audio → Spectrogram → Vision Transformer → Classification
- Treats audio as image
- Patch-based processing
- Attention over frequency-time
```

## Emotion Label Mapping

Different models may have different emotion labels:

### HuBERT-large (7 emotions)
- neutral, happy, sad, angry, fear, disgust, surprise

### SpeechBrain (4 emotions)
- neutral, happy, sad, angry

### Custom Models
- Check model card on Hugging Face
- May need label mapping

## Fine-tuning Your Own Model

If you want to train on custom data:

```python
from transformers import Wav2Vec2ForSequenceClassification, Trainer

# Load base model
model = Wav2Vec2ForSequenceClassification.from_pretrained(
    "facebook/wav2vec2-base",
    num_labels=7  # Your emotion count
)

# Prepare your dataset
# ... (data loading code)

# Train
trainer = Trainer(
    model=model,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset
)

trainer.train()
```

## Model Selection Decision Tree

```
Start
  |
  ├─ Need maximum accuracy?
  |    └─ Yes → Wav2Vec2-XLSR
  |    └─ No → Continue
  |
  ├─ Limited RAM (<4GB)?
  |    └─ Yes → SpeechBrain
  |    └─ No → Continue
  |
  ├─ Need custom emotions?
  |    └─ Yes → Wav2Vec2-base + Fine-tune
  |    └─ No → Continue
  |
  └─ Default → HuBERT-large
```

## Testing Different Models

Create a comparison script:

```python
models = [
    "superb/hubert-large-superb-er",
    "speechbrain/emotion-recognition-wav2vec2-IEMOCAP",
    "ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition"
]

for model_name in models:
    detector = EmotionDetector(model_name=model_name)
    emotion, confidence, _ = detector.predict(waveform, sr)
    print(f"{model_name}: {emotion} ({confidence:.2%})")
```

## Recommended Setup by Use Case

### Academic Project
- Model: HuBERT-large
- Reason: Standard, well-documented, good results

### Production Application
- Model: Wav2Vec2-XLSR
- Reason: Best accuracy, worth the resources

### Mobile/Edge Device
- Model: SpeechBrain or quantized HuBERT
- Reason: Smaller size, faster inference

### Research/Experimentation
- Model: Multiple models for comparison
- Reason: Understand trade-offs

## Model Updates

Models are continuously improved. Check Hugging Face for:
- New versions
- Better fine-tuned models
- Community contributions

Search: https://huggingface.co/models?pipeline_tag=audio-classification&sort=downloads

## Conclusion

**Default Recommendation: HuBERT-large**
- Best balance of accuracy, size, and speed
- Well-tested and documented
- Good for learning and production

**Alternative: SpeechBrain**
- If resources are limited
- Still good accuracy
- Faster processing

**For Best Results: Wav2Vec2-XLSR**
- When accuracy is critical
- Have sufficient resources
- Production applications

Choose based on your specific needs and constraints!
