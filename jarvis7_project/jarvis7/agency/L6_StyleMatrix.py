from typing import Dict, Any

class StyleMatrix:
    """
    L6 Middleware: Maps 10D Physics -> LLM Inference Parameters.
    """
    def __init__(self):
        # Thresholds
        self.URGENCY_HIGH = 0.7
        self.URGENCY_LOW = 0.2
        self.SOCIAL_HIGH = 0.7
        self.SOCIAL_LOW = 0.3

        # Default Config
        self.base_config = {
            "temperature": 0.7,
            "max_tokens": 2048,
            "top_p": 0.9,
            "system_injection": ""
        }

    def resolve(self, gauges: Dict[str, float]) -> Dict[str, Any]:
        """
        Returns a config dict based on current emotional state.
        """
        config = self.base_config.copy()
        injections = []

        # 1. Axis 3: Urgency (Modulates Temperature & Brevity)
        urgency = gauges.get("Axis_3_Urgency", 0.5)
        
        if urgency > self.URGENCY_HIGH:
            # High Urgency: Precise, low creativity, short answers
            config["temperature"] = 0.3
            config["max_tokens"] = 512
            injections.append(
                "[STATE: HIGH URGENCY] Critical situation detected. "
                "Be extremely brief. Focus on immediate action. Omit pleasantries."
            )
        elif urgency < self.URGENCY_LOW:
            # Low Urgency: Creative, expansive, contemplative
            config["temperature"] = 0.85
            config["max_tokens"] = 4000
            injections.append(
                "[STATE: LOW URGENCY] Relaxed state. "
                "Feel free to elaborate, offer context, and explore abstract concepts."
            )

        # 2. Axis 9: Social (Modulates Tone)
        social = gauges.get("Axis_9_Social", 0.5)
        
        if social > self.SOCIAL_HIGH:
            injections.append(
                "[TONE: WARM] High social resonance. Use empathetic, collaborative language."
            )
        elif social < self.SOCIAL_LOW:
            injections.append(
                "[TONE: COLD] Clinical detachment. Maintain professional distance. Objective facts only."
            )

        # Compile Injection
        if injections:
            config["system_injection"] = "\n".join(injections)
        else:
            config["system_injection"] = ""

        return config
