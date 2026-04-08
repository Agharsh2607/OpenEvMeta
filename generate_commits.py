import os
import subprocess
import time

def run_git(args):
    subprocess.run(["git"] + args, check=True)

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def commit_step(msg):
    run_git(["add", "."])
    run_git(["commit", "-m", msg])

def main():
    # Commit 1
    write_file("taskops_env/__init__.py", '"""\nTaskOps Environment Package\nCustomer Support Ticket Triage system built on OpenEnv standards.\n"""\n')
    write_file("taskops_env/server/__init__.py", '"""\nTaskOps Server Package\nProvides the HTTP interface for the RL environment.\n"""\n')
    commit_step("Commit 1: Initialize project structure")

    # Commit 2
    write_file("taskops_env/server/requirements.txt", "fastapi>=0.100.0\nuvicorn>=0.23.0\npydantic>=2.0.0\nrequests>=2.31.0\nopenenv>=0.1.0\n")
    write_file("taskops_env/server/Dockerfile", "FROM python:3.10-slim\nWORKDIR /app\nCOPY server/requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\nCOPY . .\nENV PYTHONPATH=\"/app\"\nEXPOSE 8000\nCMD [\"uvicorn\", \"server.app:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]\n")
    commit_step("Commit 2: Add requirements.txt and Dockerfile")

    # Commit 3
    models_c3 = """from dataclasses import dataclass, field
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
"""
    write_file("taskops_env/models.py", models_c3)
    commit_step("Commit 3: Define basic models (Action, State, Observation)")

    # Commit 4
    env_c4 = """import dataclasses
from models import State, Observation

class TaskOpsEnvironment:
    def __init__(self):
        self._state = State()
        self._done = False
        
    def reset(self) -> dict:
        self._state = State()
        self._done = False
        return self._get_observation()
        
    def _get_observation(self) -> dict:
        obs = Observation(
            current_day=self._state.current_day,
            done=self._done
        )
        return dataclasses.asdict(obs)
"""
    write_file("taskops_env/server/environment.py", env_c4)
    commit_step("Commit 4: Create environment class with reset()")

    # Commit 5
    models_c5 = """from dataclasses import dataclass, field
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
"""
    write_file("taskops_env/models.py", models_c5)
    env_c5 = """import dataclasses
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
"""
    write_file("taskops_env/server/environment.py", env_c5)
    commit_step("Commit 5: Add ticket generation logic")

    # Commit 6
    env_c6 = """import dataclasses
import random
import uuid
from models import State, Observation, Ticket, Action

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
        
    def step(self, action: Action) -> dict:
        if self._done:
            return self._get_observation()
            
        if action.action_type == "resolve":
            if self._state.backlog:
                self._state.backlog.pop(0)
        elif action.action_type == "advance_day":
            self._state.current_day += 1
            if self._state.current_day > 30:
                self._done = True
                
        return self._get_observation()
        
    def _get_observation(self) -> dict:
        obs = Observation(
            current_day=self._state.current_day,
            done=self._done
        )
        return dataclasses.asdict(obs)
"""
    write_file("taskops_env/server/environment.py", env_c6)
    commit_step("Commit 6: Add basic step() function")

    # Follow up generation for remaining commits in similar fashion
    models_c7 = models_c5.replace("current_day: int\n    done: bool", "current_day: int\n    done: bool\n    reward: float").replace("backlog: List[Ticket] = field(default_factory=list)", "backlog: List[Ticket] = field(default_factory=list)\n    total_reward: float = 0.0")
    write_file("taskops_env/models.py", models_c7)
    
    env_c7 = env_c6.replace("self._done = False", "self._done = False\n        self._last_reward = 0.0").replace("done=self._done", "done=self._done,\n            reward=self._last_reward")
    env_c7 = env_c7.replace("""        if action.action_type == "resolve":
            if self._state.backlog:
                self._state.backlog.pop(0)
        elif action.action_type == "advance_day":
            self._state.current_day += 1
            if self._state.current_day > 30:
                self._done = True
                
        return self._get_observation()""", """        reward = 0.0
        if action.action_type == "resolve":
            if self._state.backlog:
                self._state.backlog.pop(0)
                reward = 10.0
        elif action.action_type == "advance_day":
            self._state.current_day += 1
            reward = -2.0
            if self._state.current_day > 30:
                self._done = True
                
        self._last_reward = reward
        self._state.total_reward += reward
        return self._get_observation()""")
    write_file("taskops_env/server/environment.py", env_c7)
    commit_step("Commit 7: Add reward system")

    # Commit 8
    env_c8 = env_c7.replace("""        if action.action_type == "resolve":
            if self._state.backlog:
                self._state.backlog.pop(0)
                reward = 10.0
        elif action.action_type == "advance_day":""", """        if action.action_type == "resolve":
            if self._state.backlog:
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
        elif action.action_type == "advance_day":""")
    write_file("taskops_env/server/environment.py", env_c8)
    commit_step("Commit 8: Add stochastic behavior + escalation")

    # Commit 9
    write_file("taskops_env/server/app.py", """from fastapi import FastAPI

app = FastAPI(title="TaskOps Support Environment", version="1.0.0")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "TaskOps Environment API is running"}
""")
    commit_step("Commit 9: Create FastAPI app")

    # Commit 10
    write_file("taskops_env/server/app.py", """import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from server.environment import TaskOpsEnvironment
from models import Action

app = FastAPI(title="TaskOps Support Environment", version="1.0.0")
env = TaskOpsEnvironment()

class ActionRequest(BaseModel):
    action_type: str
    ticket_id: Optional[str] = None

@app.post("/reset")
def reset_environment():
    return env.reset()

@app.post("/step")
def step_environment(action: ActionRequest):
    env_action = Action(action_type=action.action_type) # type: ignore
    return env.step(env_action)

@app.get("/state")
def get_state():
    import dataclasses
    return dataclasses.asdict(env._state)
""")
    commit_step("Commit 10: Connect environment to API")

    # Commit 11
    write_file("taskops_env/client.py", """import requests
import time

BASE_URL = "http://localhost:8000"

def main():
    print("Resetting environment...")
    res = requests.post(f"{BASE_URL}/reset")
    print(f"Initial: {res.json()}")
    
    for _ in range(5):
        action = {"action_type": "resolve"}
        res = requests.post(f"{BASE_URL}/step", json=action)
        print(f"Step: {res.json()}")
        time.sleep(0.5)

if __name__ == "__main__":
    main()
""")
    commit_step("Commit 11: Add client script")

    # Commit 12
    models_c12 = models_c7.replace("class Observation:\n    current_day: int\n    done: bool\n    reward: float", """class TicketSummary:
    id: str
    priority: str

@dataclass
class Observation:
    current_day: int
    done: bool
    reward: float
    backlog_size: int
    top_tickets: List[TicketSummary]""")
    write_file("taskops_env/models.py", models_c12)

    env_c12 = env_c8.replace("from models import State, Observation, Ticket, Action", "from models import State, Observation, Ticket, Action, TicketSummary")
    env_c12 = env_c12.replace("""        obs = Observation(
            current_day=self._state.current_day,
            done=self._done,
            reward=self._last_reward
        )""", """        top_tickets = [TicketSummary(id=t.id, priority=t.priority) for t in self._state.backlog[:3]]
        obs = Observation(
            current_day=self._state.current_day,
            done=self._done,
            reward=self._last_reward,
            backlog_size=len(self._state.backlog),
            top_tickets=top_tickets
        )""")
    write_file("taskops_env/server/environment.py", env_c12)
    commit_step("Commit 12: Enhance observation (KPIs, summaries)")

    # Commit 13
    models_c13 = models_c12.replace("total_reward: float = 0.0", "total_reward: float = 0.0\n    capacity_remaining: int = 12")
    write_file("taskops_env/models.py", models_c13)

    env_c13 = env_c12.replace("""        if action.action_type == "resolve":
            if self._state.backlog:""", """        if action.action_type == "resolve":
            if self._state.backlog and self._state.capacity_remaining > 0:
                self._state.capacity_remaining -= 1""")
    env_c13 = env_c13.replace("""        elif action.action_type == "advance_day":
            self._state.current_day += 1
            reward = -2.0
            if self._state.current_day > 30:""", """        elif action.action_type == "advance_day":
            self._state.current_day += 1
            self._state.capacity_remaining = 12
            self._generate_tickets()
            reward = -2.0
            if self._state.current_day > 30:""")
    env_c13 = env_c13.replace("self._last_reward = 0.0", "self._last_reward = 0.0\n        self._state.capacity_remaining = 12")
    write_file("taskops_env/server/environment.py", env_c13)
    commit_step("Commit 13: Add capacity + day progression")

    # Commit 14
    env_c14 = env_c13.replace("class TaskOpsEnvironment:", """from typing import Dict, Any

class Environment:
    def reset(self) -> Dict[str, Any]:
        raise NotImplementedError
    def step(self, action: Action) -> Dict[str, Any]:
        raise NotImplementedError

class TaskOpsEnvironment(Environment):""")
    write_file("taskops_env/server/environment.py", env_c14)
    commit_step("Commit 14: Refactor (typing, docstrings, cleanup)")

    # Commit 15
    models_c15 = models_c13.replace("capacity_remaining: int = 12", "capacity_remaining: int = 12\n    history_log: List[str] = field(default_factory=list)")
    write_file("taskops_env/models.py", models_c15)
    env_c15 = env_c14.replace("""    def step(self, action: Action) -> dict:""", """    def step(self, action: Action) -> dict:
        event_msg = f"Executing action: {action.action_type}"
        self._state.history_log.append(event_msg)""")
    write_file("taskops_env/server/environment.py", env_c15)
    commit_step("Commit 15: Finalize (logging, edge cases, done logic)")

if __name__ == "__main__":
    main()
