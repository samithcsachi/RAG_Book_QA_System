from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="RAG Book QA System API",
    docs_url="/docs"
)
app.include_router(router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
