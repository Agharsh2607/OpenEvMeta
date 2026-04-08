from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
from environment import TaskOpsEnvironment
from models import Action
from services.aiService import ai_service
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

# --- AI Integration UI Module ---

@app.get("/", response_class=HTMLResponse)
def get_ui():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>TaskOps - AI Operations Hub</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0d1117; color: #c9d1d9; padding: 40px; margin: 0; display: flex; justify-content: center; }
            .container { background: #161b22; padding: 30px; border-radius: 10px; border: 1px solid #30363d; width: 100%; max-width: 600px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
            h2 { font-weight: 600; margin-top: 0; color: #58a6ff; }
            input { width: calc(100% - 22px); padding: 10px; margin-bottom: 10px; border-radius: 5px; border: 1px solid #30363d; background: #0d1117; color: #c9d1d9; }
            button { width: 100%; padding: 10px; border: none; border-radius: 5px; background: #238636; color: white; cursor: pointer; font-weight: bold; transition: 0.2s; }
            button:hover { background: #2ea043; }
            button:disabled { background: #21262d; cursor: not-allowed; }
            .status { margin-top: 15px; font-size: 0.9em; color: #8b949e; }
            .output { margin-top: 10px; padding: 15px; border-radius: 5px; background: #0d1117; border: 1px solid #30363d; min-height: 80px; overflow-x: auto; font-family: monospace; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>TaskOps AI Operations Hub</h2>
            <p style="font-size: 0.9em; color: #8b949e;">Query models powered natively by Hugging Face via API endpoints dynamically.</p>
            <input type="text" id="query" placeholder="Ask AI... (e.g. Can you summarize the system state?)" autocomplete="off">
            <button id="submitBtn" onclick="askAI()">Analyze via HuggingFace</button>
            <div class="status" id="status">Ready</div>
            <div class="output" id="result">&gt; Waiting for prompt...</div>
        </div>
        
        <script>
            async function askAI() {
                const query = document.getElementById('query').value;
                if (!query) return;
                
                const btn = document.getElementById('submitBtn');
                const status = document.getElementById('status');
                const result = document.getElementById('result');
                
                btn.disabled = true;
                status.innerText = 'Calling Hugging Face Inference Node...';
                result.innerText = '';
                
                try {
                    const res = await fetch('/api/ai_action', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({query})
                    });
                    const data = await res.json();
                    result.innerText = JSON.stringify(data, null, 2);
                    status.innerText = 'Execution Complete';
                } catch(e) {
                    result.innerText = 'Error: ' + e;
                    status.innerText = 'Execution Failed';
                } finally {
                    btn.disabled = false;
                }
            }
        </script>
    </body>
    </html>
    """
    return html_content

class AIQueryRequest(BaseModel):
    query: str

@app.post("/api/ai_action")
async def execute_ai_action(req: AIQueryRequest):
    res = await ai_service.process_inference(req.query)
    return {"huggingface_response": res}
