from dataclasses import dataclass, field
from typing import Dict

@dataclass
class ValueSystem:
    core_values: Dict[str, float] = field(
        default_factory=lambda: {
            "efficiency": 1.0,
            "safety": 1.0,
            "curiosity": 0.9,
            "autonomy": 0.8
        }
    )
