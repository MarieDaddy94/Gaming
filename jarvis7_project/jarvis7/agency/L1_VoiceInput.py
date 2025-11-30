class VoiceReceptor:
    """
    L1 Subsystem: Semantic & Prosodic Hearing.
    Infers physical intensity from input characteristics.
    """
    def __init__(self):
        pass

    def listen(self, raw_text: str):
        """
        Analyzes text for 'volume' (caps, punctuation).
        Returns: (clean_text, intensity_float)
        """
        if not raw_text:
            return "", 0.0

        intensity = 0.2 # Base baseline

        # Heuristic: Exclamation marks increase intensity
        intensity += (raw_text.count("!") * 0.2)

        # Heuristic: ALL CAPS implies shouting/urgency
        # Check if a significant portion is upper case
        alphachars = [c for c in raw_text if c.isalpha()]
        if alphachars:
            upper_count = sum(1 for c in alphachars if c.isupper())
            ratio = upper_count / len(alphachars)
            if ratio > 0.6:
                intensity += 0.4

        # Clamp between 0.0 and 1.0
        intensity = min(1.0, max(0.0, intensity))
        
        return raw_text, intensity

    def process_physics(self, intensity: float) -> dict:
        """
        Prepares the stimulus packet for the Global Workspace / State.
        """
        return {
            "channel": "auditory",
            "stimulus_type": "voice",
            "intensity": intensity,
            "axis_mapping": "Axis_6_InputIntensity"
        }
