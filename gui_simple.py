"""
Simple GUI for Voice Emotion Detection using Tkinter
Run: python gui_simple.py
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import sys
from pathlib import Path
import threading

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.emotion_detector import EmotionDetector
from src.audio_processor import AudioProcessor


class EmotionDetectorGUI:
    """Simple GUI for emotion detection"""
    
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Voice Emotion Detector")
        self.window.geometry("600x500")
        self.window.resizable(False, False)
        
        # Initialize components (lazy loading)
        self.detector = None
        self.audio_processor = AudioProcessor()
        self.current_file = None
        
        # Emotion emoji mapping
        self.emoji_map = {
            'happy': '😊',
            'sad': '😢',
            'angry': '😠',
            'neutral': '😐',
            'fear': '😨',
            'disgust': '🤢',
            'surprise': '😲'
        }
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # Title
        title_frame = tk.Frame(self.window, bg="#2c3e50", height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🎤 Voice Emotion Detector",
            font=("Arial", 24, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Main content frame
        content_frame = tk.Frame(self.window, bg="#ecf0f1")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # File selection section
        file_frame = tk.Frame(content_frame, bg="#ecf0f1")
        file_frame.pack(pady=10)
        
        self.file_label = tk.Label(
            file_frame,
            text="No file selected",
            font=("Arial", 11),
            bg="#ecf0f1",
            fg="#7f8c8d"
        )
        self.file_label.pack(pady=5)
        
        select_btn = tk.Button(
            file_frame,
            text="📁 Select Audio File",
            command=self.select_file,
            font=("Arial", 12),
            bg="#3498db",
            fg="white",
            padx=20,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2"
        )
        select_btn.pack(pady=5)
        
        # Analyze button
        self.analyze_btn = tk.Button(
            content_frame,
            text="🔍 Analyze Emotion",
            command=self.analyze_audio,
            font=("Arial", 14, "bold"),
            bg="#27ae60",
            fg="white",
            padx=30,
            pady=15,
            relief=tk.FLAT,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.analyze_btn.pack(pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            content_frame,
            mode='indeterminate',
            length=400
        )
        
        # Status label
        self.status_label = tk.Label(
            content_frame,
            text="",
            font=("Arial", 10),
            bg="#ecf0f1",
            fg="#7f8c8d"
        )
        self.status_label.pack(pady=5)
        
        # Result frame
        self.result_frame = tk.Frame(content_frame, bg="#ecf0f1")
        self.result_frame.pack(pady=20)
        
        # Footer
        footer = tk.Label(
            self.window,
            text="Powered by Hugging Face Transformers",
            font=("Arial", 9),
            bg="#ecf0f1",
            fg="#95a5a6"
        )
        footer.pack(side=tk.BOTTOM, pady=10)
        
    def select_file(self):
        """Open file dialog to select audio file"""
        file_path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[
                ("Audio Files", "*.wav *.mp3 *.flac *.ogg"),
                ("WAV Files", "*.wav"),
                ("MP3 Files", "*.mp3"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            self.current_file = file_path
            filename = Path(file_path).name
            self.file_label.config(
                text=f"Selected: {filename}",
                fg="#2c3e50"
            )
            self.analyze_btn.config(state=tk.NORMAL)
            
            # Clear previous results
            for widget in self.result_frame.winfo_children():
                widget.destroy()
    
    def analyze_audio(self):
        """Analyze the selected audio file"""
        if not self.current_file:
            messagebox.showwarning("No File", "Please select an audio file first")
            return
        
        # Disable button during processing
        self.analyze_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Processing...")
        self.progress.pack(pady=10)
        self.progress.start(10)
        
        # Run in separate thread to keep GUI responsive
        thread = threading.Thread(target=self._process_audio)
        thread.start()
    
    def _process_audio(self):
        """Process audio in background thread"""
        try:
            # Load model if not loaded
            if not self.detector:
                self.update_status("Loading model (first time only)...")
                self.detector = EmotionDetector(use_gpu=False)
            
            # Process audio
            self.update_status("Loading audio...")
            waveform, sr = self.audio_processor.load_audio(self.current_file)
            
            self.update_status("Preprocessing...")
            waveform = self.audio_processor.preprocess_audio(waveform, sr)
            
            # Validate quality
            is_valid, msg = self.audio_processor.validate_audio_quality(waveform)
            if not is_valid:
                self.show_error(msg)
                return
            
            # Predict
            self.update_status("Analyzing emotion...")
            emotion, confidence, all_scores = self.detector.predict(waveform, sr)
            
            # Show results in main thread
            self.window.after(0, self.show_results, emotion, confidence, all_scores)
            
        except Exception as e:
            self.show_error(str(e))
    
    def update_status(self, message):
        """Update status label (thread-safe)"""
        self.window.after(0, self.status_label.config, {"text": message})
    
    def show_error(self, error_msg):
        """Show error message"""
        self.window.after(0, self._show_error_dialog, error_msg)
    
    def _show_error_dialog(self, error_msg):
        """Show error dialog in main thread"""
        self.progress.stop()
        self.progress.pack_forget()
        self.status_label.config(text="")
        self.analyze_btn.config(state=tk.NORMAL)
        messagebox.showerror("Error", f"Failed to process audio:\n{error_msg}")
    
    def show_results(self, emotion, confidence, all_scores):
        """Display results in GUI"""
        # Stop progress bar
        self.progress.stop()
        self.progress.pack_forget()
        self.status_label.config(text="Analysis complete!")
        self.analyze_btn.config(state=tk.NORMAL)
        
        # Clear previous results
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        # Get emoji
        emoji = self.emoji_map.get(emotion.lower(), '🎭')
        
        # Main result
        result_label = tk.Label(
            self.result_frame,
            text=f"{emoji} {emotion.upper()}",
            font=("Arial", 32, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        result_label.pack(pady=10)
        
        # Confidence
        confidence_label = tk.Label(
            self.result_frame,
            text=f"Confidence: {confidence*100:.1f}%",
            font=("Arial", 16),
            bg="#ecf0f1",
            fg="#27ae60" if confidence > 0.7 else "#f39c12"
        )
        confidence_label.pack(pady=5)
        
        # Confidence level
        if confidence > 0.7:
            level = "HIGH ✓✓✓"
            color = "#27ae60"
        elif confidence > 0.4:
            level = "MEDIUM ✓✓"
            color = "#f39c12"
        else:
            level = "LOW ✓"
            color = "#e74c3c"
        
        level_label = tk.Label(
            self.result_frame,
            text=f"Confidence Level: {level}",
            font=("Arial", 11),
            bg="#ecf0f1",
            fg=color
        )
        level_label.pack(pady=5)
        
        # Top 3 emotions
        separator = tk.Frame(self.result_frame, height=2, bg="#bdc3c7")
        separator.pack(fill=tk.X, pady=10)
        
        top_label = tk.Label(
            self.result_frame,
            text="Top 3 Predictions:",
            font=("Arial", 11, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        top_label.pack(pady=5)
        
        # Sort and show top 3
        sorted_scores = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        
        for i, (emo, score) in enumerate(sorted_scores, 1):
            emo_emoji = self.emoji_map.get(emo.lower(), '🎭')
            score_text = f"{i}. {emo_emoji} {emo.capitalize()}: {score*100:.1f}%"
            
            score_label = tk.Label(
                self.result_frame,
                text=score_text,
                font=("Arial", 10),
                bg="#ecf0f1",
                fg="#34495e"
            )
            score_label.pack(pady=2)
    
    def run(self):
        """Start the GUI"""
        self.window.mainloop()


if __name__ == "__main__":
    print("Starting Voice Emotion Detector GUI...")
    print("Note: Model will be downloaded on first run (may take a few minutes)")
    
    app = EmotionDetectorGUI()
    app.run()
