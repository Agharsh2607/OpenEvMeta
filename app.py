from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from environment import TaskOpsEnvironment
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
