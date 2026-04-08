def grade(state, **kwargs) -> float:
    backlog = state.get("backlog", [])
    if not backlog:
        return 1.0
    overdue = sum(1 for t in backlog if t.get("sla_deadline", 0) < 0)
    val = 1.0 - (overdue / len(backlog))
    return float(max(0.0, min(1.0, val)))
