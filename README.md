<div align="center">
  <h1>🎫 TaskOps: Customer Support Triage</h1>
  <p><strong>A Highly Realistic Reinforcement Learning Environment for Ticket Triage & Resolution</strong></p>
  
  [![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org)
  [![FastAPI](https://img.shields.io/badge/Framework-FastAPI-009688.svg)](https://fastapi.tiangolo.com)
  [![OpenEnv](https://img.shields.io/badge/Environment-OpenEnv-orange.svg)](https://github.com/openenv/)
</div>

<hr/>

## 🎯 Overview

**TaskOps** is a production-ready Web environment mimicking a complex Software-as-a-Service (SaaS) customer support center. Built on the **OpenEnv** framework, the environment requires an autonomous RL agent to handle endless influxes of dynamically generated customer support tickets. 

The goal? **Minimize SLA breaches and mitigate enterprise customer churn while working efficiently under extremely limited capacity pipelines.**

---

## 🧠 Environment Characteristics

Each episode simulates exactly **30 action-packed days** at a fast-paced SaaS startup. 

### 🔧 Ticket Dynamics
Tickets arrive randomly with varied weights:
* **Priority Levels:** `low`, `medium`, `high`, `critical`
* **Company Status:** `free`, `pro`, `enterprise` (higher churn probability)
* **Demands:** Randomly assigned *Estimated Efforts* mapping to resolution complexity.
* **Ticking Clocks:** Hard SLAs that penalize heavily when breached.

### 🎮 The Action Space
On each step, the Agent decides exactly one course of action:
- `assign` — Moves the ticket closer to designated teams.
- `resolve` — Burns daily human capacity trying to solve the problem (features a stochastic success roll based on effort difficulty).
- `escalate` — Safely grants a 3-day SLA extension but permanently hits the reward mechanism.
- `advance_day` — Skips to the next day when resources run completely dry.
- `defer` — Delays execution intentionally.

### 📊 Reward Architecture
Rewards are continuously formulated and calculated through dynamic endpoint interactions:
* ✅ **Positive Flow:** Successfully dispatching complex metrics + priority enterprise saves.
* ❌ **Negative Drawdown:** SLA violations, backlog buildup, heavy escalation costs, and dreaded outright total churn.

---

## 🚀 Getting Started

Launch an instance using native Python binaries or completely containerized structures:

### 🐳 Docker Native
```bash
docker build -t taskops-env .
docker run -p 8000:8000 taskops-env
```

### 🐍 Standard Boot
```bash
pip install -r requirements.txt
uvicorn app:app --port 8000
```

---

## 🤖 Running Inference

This project includes a bundled API-compliant testing module utilizing an OpenAI client shim exactly matching standard OpenEnv evaluation frameworks!

```bash
export API_BASE_URL="http://localhost:8000"
export MODEL_NAME="gpt-4o"
python inference.py
```

<br/>
<div align="center">
  <i>Built with ❤️ for OpenEnv RL Architectures.</i>
</div>
