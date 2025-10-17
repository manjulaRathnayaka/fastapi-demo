from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse
from datetime import datetime
import logging

app = FastAPI(title="FastAPI Demo", version="1.0.0")

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
log = logging.getLogger("app")

@app.middleware("http")
async def access_log(request: Request, call_next):
    start = datetime.now()
    resp = await call_next(request)
    dur_ms = (datetime.now() - start).total_seconds() * 1000
    log.info("path=%s method=%s status=%s dur_ms=%.2f",
             request.url.path, request.method, resp.status_code, dur_ms)
    return resp

@app.get("/health")
def health():
    return {"status": "ok", "message": "Hello PyCon!"}

@app.get("/score")
def score(text: str = Query(..., min_length=1, description="Text to score")):
    return {"text": text, "score": len(text) % 10}

