# Local TextRank Research Summarizer

Fully local two-service system:
- `main_app` (Flask UI/client)
- `model_service` (FastAPI TextRank model API)

No external summarization APIs or pretrained summarization pipelines are used.

## Architecture

User -> Flask app -> HTTP POST -> FastAPI model service -> TextRank pipeline -> response -> Flask UI.

## Folder Structure

```
main_app/
  app.py
  client.py
  templates/
    index.html

model_service/
  api.py
  preprocessing.py
  vectorization.py
  similarity.py
  ranking.py
  pipeline.py
```

## TextRank Pipeline

1. Sentence preprocessing
2. TF-IDF vectorization
3. Cosine similarity matrix
4. Graph construction
5. PageRank scoring
6. Top-N sentence extraction
7. Reorder sentences by original position
8. Build final summary

## Setup

```bash
cd prjoect_exhibition-2
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Optional `.env`:

```
MODEL_SERVICE_URL=http://127.0.0.1:8001
```

## Run (two terminals)

Terminal 1:
```bash
python run_model_service.py
```

Terminal 2:
```bash
python run.py
```

Open `http://127.0.0.1:5000`.

## Model Service API

`POST /summarize`

Request:
```json
{
  "text": "full research text...",
  "num_sentences": 5
}
```

Response:
```json
{
  "summary": "...",
  "selected_sentences": ["...", "..."],
  "processing_time": 0.1234
}
```
# AI_research_paper_summariser
# AI_research_paper_summariser
