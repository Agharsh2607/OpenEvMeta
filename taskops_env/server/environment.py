import dataclasses
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
