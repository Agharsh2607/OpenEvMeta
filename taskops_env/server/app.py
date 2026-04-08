from fastapi import FastAPI

app = FastAPI(title="TaskOps Support Environment", version="1.0.0")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "TaskOps Environment API is running"}
