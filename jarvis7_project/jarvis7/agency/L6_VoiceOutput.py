import os
from typing import Dict
from .L6_StyleMatrix import StyleMatrix

class VoiceEmitter:
    """
    L6 Subsystem: Affective Voice Synthesis.
    Controls Prosody (speed, pitch stability) based on internal state.
    """
    def __init__(self, style_matrix: StyleMatrix = None):
        self.style_matrix = style_matrix or StyleMatrix()
        # You could plug a real TTS client here
        # self.client = ElevenLabsClient(...) 

    def speak(self, text: str, gauges: Dict[str, float]) -> None:
        """
        Simulates speaking by calculating voice parameters from physics.
        """
        # Resolve style to get the "vibe"
        style_cfg = self.style_matrix.resolve(gauges)
        
        urgency = gauges.get("Axis_3_Urgency", 0.5)
        social = gauges.get("Axis_9_Social", 0.5)

        # Calculate Prosody
        speed = 1.0
        stability = 0.5 # 0 = expressive/erratic, 1 = monotone/stable

        if urgency > 0.7:
            speed = 1.25     # Talk faster
            stability = 0.8  # More rigid/military
        elif social > 0.7:
            speed = 0.9      # Talk slightly slower (warmer)
            stability = 0.3  # Very expressive

        # Since we are in a Docker container, we log the intent to speak.
        # The Dashboard/Frontend would handle the actual audio generation.
        print(f"\n🔊 [VOICE OUT] '{text}'")
        print(f"   [Params] Speed: {speed:.2f} | Stability: {stability:.2f} | Injection: {style_cfg.get('system_injection')[:50]}...")

    def generate_audio_file(self, text: str):
        # Placeholder for actual .mp3 generation logic
        pass
