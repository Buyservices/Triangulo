from fastapi import FastAPI
from app.interfaces.http.api.v1.routers import router as v1_router

app = FastAPI(title="API Vendas - Newcon Bridge (HTTP NEW)", version="1.0.0")

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(v1_router, prefix="/v1")
