def grade(state, **kwargs) -> float:
    backlog = state.get("backlog", [])
    # 0 backlog = 1.0, 10+ backlog = 0.0
    val = 1.0 - (len(backlog) / 10.0)
    return float(max(0.0, min(1.0, val)))
