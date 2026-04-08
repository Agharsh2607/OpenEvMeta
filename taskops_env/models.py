from dataclasses import dataclass, field
from typing import Literal

@dataclass
class Action:
    action_type: Literal["assign", "resolve", "escalate", "defer", "advance_day"]

@dataclass
class Observation:
    current_day: int
    done: bool

@dataclass
class State:
    current_day: int = 1
