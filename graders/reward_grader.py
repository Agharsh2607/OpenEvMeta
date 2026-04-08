def grade(state, **kwargs) -> float:
    reward = state.get("total_reward", 0.0)
    # Normalize reward to 0-1 range roughly. If reward >= 50 -> 1.0, if < 0 -> 0.0
    val = reward / 50.0
    return float(max(0.0, min(1.0, val)))
