"""FastAPI app exposing local TextRank model service."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from model_service.pipeline import summarize_text_textrank

app = FastAPI(title="Local TextRank Model Service")


class SummarizeRequest(BaseModel):
    text: str = Field(..., description="Full research text")
    num_sentences: int = Field(5, ge=1, le=20)


class SummarizeResponse(BaseModel):
    summary: str
    selected_sentences: list[str]
    processing_time: float


@app.get("/health")
def health():
    return {"status": "ok", "service": "model_service"}


@app.post("/summarize", response_model=SummarizeResponse)
def summarize(req: SummarizeRequest):
    text = req.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Input text is empty.")
    result = summarize_text_textrank(text=text, num_sentences=req.num_sentences)
    return SummarizeResponse(**result)
