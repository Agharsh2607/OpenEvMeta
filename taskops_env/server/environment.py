import dataclasses
import random
import uuid
from models import State, Observation, Ticket, Action, TicketSummary

from typing import Dict, Any

class Environment:
    def reset(self) -> Dict[str, Any]:
        raise NotImplementedError
    def step(self, action: Action) -> Dict[str, Any]:
        raise NotImplementedError

class TaskOpsEnvironment(Environment):
    def __init__(self):
        self._state = State()
        self._done = False
        self._last_reward = 0.0
        self._state.capacity_remaining = 12
        
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
        self._last_reward = 0.0
        self._state.capacity_remaining = 12
        self._generate_tickets()
        return self._get_observation()
        
    def step(self, action: Action) -> dict:
        if self._done:
            return self._get_observation()
            
        reward = 0.0
        if action.action_type == "resolve":
            if self._state.backlog and self._state.capacity_remaining > 0:
                self._state.capacity_remaining -= 1
                if random.random() < 0.8:
                    self._state.backlog.pop(0)
                    reward = 10.0
                else:
                    reward = -1.0
        elif action.action_type == "escalate":
            if self._state.backlog:
                ticket = self._state.backlog[0]
                ticket.sla_deadline += 3
                reward = -5.0
        elif action.action_type == "advance_day":
            self._state.current_day += 1
            self._state.capacity_remaining = 12
            self._generate_tickets()
            reward = -2.0
            if self._state.current_day > 30:
                self._done = True
                
        self._last_reward = reward
        self._state.total_reward += reward
        return self._get_observation()
        
    def _get_observation(self) -> dict:
        top_tickets = [TicketSummary(id=t.id, priority=t.priority) for t in self._state.backlog[:3]]
        obs = Observation(
            current_day=self._state.current_day,
            done=self._done,
            reward=self._last_reward,
            backlog_size=len(self._state.backlog),
            top_tickets=top_tickets
        )
        return dataclasses.asdict(obs)
