from dataclasses import dataclass, field
from typing import Literal, List

@dataclass
class Ticket:
    id: str
    priority: Literal["low", "medium", "high", "critical"]
    customer_tier: Literal["free", "pro", "enterprise"]
    estimated_effort: int
    sla_deadline: int

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
    backlog: List[Ticket] = field(default_factory=list)
