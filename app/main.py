from fastapi import FastAPI
from app.api.transcripts import router as transcripts_router
from app.api.queries import router as queries_router

app = FastAPI(title="LLM Transcript Analyzer + RAG Summarizer")

app.include_router(transcripts_router, prefix="/transcripts", tags=["Transcripts"])
app.include_router(queries_router, prefix="/queries", tags=["Queries"])


@app.get("/")
async def root():
    return {"message": "LLM Transcript Analyzer is running"}

# Run the app with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)