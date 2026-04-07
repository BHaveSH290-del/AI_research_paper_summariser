# System Architecture

## Module Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     FRONTEND LAYER (UI)                          │
│  • File upload • Submit button • Loading indicator               │
│  • Summary display • Error display                               │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTP (fetch/AJAX)
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                     BACKEND API LAYER                            │
│  • FastAPI routes • Request validation • Response formatting     │
│  • Health check • File upload handling • CORS                    │
└──────────────────────────┬──────────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
┌──────────────────┐ ┌──────────────┐ ┌──────────────────────────┐
│ PDF PROCESSING   │ │   CHUNKING   │ │ AI SUMMARIZATION LAYER   │
│ LAYER            │ │   STRATEGY   │ │                          │
│ • Extract text   │ │ • Smart      │ │ • Model loading          │
│ • Page-by-page   │ │   chunking   │ │ • Recursive summarization│
│ • Structural     │ │ • Sentence   │ │ • CPU inference          │
│   detection      │ │   boundaries │ │ • Configurable params    │
└──────────────────┘ └──────────────┘ └──────────────────────────┘
```

## Separation of Concerns

| Layer | Responsibility |
|-------|----------------|
| **Frontend** | User interaction, display, loading states |
| **Backend API** | Routing, validation, orchestration |
| **PDF Processing** | Text extraction, cleaning, structure detection |
| **AI Summarization** | Model inference, chunk summarization, recursion |

## Data Flow

1. User uploads PDF → API validates → PDF Layer extracts text
2. Text → Preprocessing → Token estimation → Chunking
3. Chunks → AI Layer (per-chunk summary) → Combine
4. If combined too long → Recursive summarization → Final summary
5. API returns JSON → Frontend displays
