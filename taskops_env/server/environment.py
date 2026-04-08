import dataclasses
import random
import uuid
from models import State, Observation, Ticket

class TaskOpsEnvironment:
    def __init__(self):
        self._state = State()
        self._done = False
        
    def _generate_tickets(self):
        num_new = random.randint(2, 6)
        for _ in range(num_new):
            ticket = Ticket(
                id=str(uuid.uuid4())[:8],
                priority=random.choice(["low", "medium", "high", "critical"]),
                customer_tier=random.choice(["free", "pro", "enterprise"]),
                estimated_effort=random.randint(1, 5),
                sla_deadline=random.randint(1, 7)
            )
            self._state.backlog.append(ticket)

    def reset(self) -> dict:
        self._state = State()
        self._done = False
        self._generate_tickets()
        return self._get_observation()
        
    def _get_observation(self) -> dict:
        obs = Observation(
            current_day=self._state.current_day,
            done=self._done
        )
        return dataclasses.asdict(obs)
