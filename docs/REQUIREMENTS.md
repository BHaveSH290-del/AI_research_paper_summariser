# AI Research Paper Summarizer — Requirements Specification

## Functional Requirements

| ID | Requirement | Description |
|----|-------------|-------------|
| FR-1 | Upload research paper | Accept PDF files only for upload |
| FR-2 | Extract full readable text | Extract complete text content from PDF documents |
| FR-3 | Handle long documents | Safely process documents up to 30–40 pages without crash |
| FR-4 | Generate AI-based summary | Produce coherent summaries using local AI model |
| FR-5 | Display summary in browser | Render summary in clean, readable format |
| FR-6 | Summarization via API | Uses OpenAI API for fast summarization (no local model) |
| FR-7 | Graceful error handling | Structured error messages for all failure modes |

**Reason:** Prevents scope creep. Clear boundaries.

---

## Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-1 | No local model | Uses OpenAI API; no GPU or heavy CPU inference |
| NFR-2 | Document size | Handle up to 30–40 page PDFs |
| NFR-3 | Stability | Must not crash on long inputs |
| NFR-4 | Non-blocking UI | Processing must not block user interface |
| NFR-5 | Modular structure | Clean separation of concerns |

**Reason:** Real systems fail on non-functional constraints, not features.
