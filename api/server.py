from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Jarvis API", version="1.0.0")


@app.get("/")
def home():
    return {"ok": True, "service": "jarvis-api"}


@app.get("/health")
def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("api.server:app", host="0.0.0.0", port=8000, reload=False)
