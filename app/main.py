from fastapi import FastAPI

app = FastAPI(
    title="CS Cloud Backend",
    description="CS云炼金后台API",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "status": "running",
        "service": "CS Cloud Backend"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }