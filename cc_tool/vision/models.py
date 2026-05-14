from dataclasses import dataclass
from typing import Optional

@dataclass
class ReactionResult:
    event_index: int
    reaction_type: str
    confidence: float
    frame_path: Optional[str]

    def to_dict(self) -> dict:
        return {
            "event_index": self.event_index,
            "reaction_type": self.reaction_type,
            "confidence": round(self.confidence, 4),
            "frame_path": self.frame_path,
        }
