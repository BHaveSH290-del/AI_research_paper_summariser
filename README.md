# 📄 AI Research Paper Summariser

A **fully local**, two-service text summarization system built around the **TextRank algorithm**. No external summarization APIs, no pretrained summarization models — just classical NLP running entirely on your machine.

---

## 🧠 What Is This?

This project summarizes long research papers or any large body of text by extracting the most important sentences — not generating new ones. It uses **TextRank**, a graph-based ranking algorithm inspired by Google's PageRank, applied to sentences.

The result is an **extractive summary**: a set of original sentences from the input text, selected and reordered to form a coherent, concise summary.

---

## 🏗️ System Architecture

The system is split into two independent services that communicate over HTTP:

```
User (Browser)
     │
     ▼
┌─────────────────────────┐
│   main_app  (Flask)     │  ← Port 5000
│   Web UI + HTTP Client  │
└────────────┬────────────┘
             │  POST /summarize  (JSON)
             ▼
┌─────────────────────────┐
│  model_service (FastAPI)│  ← Port 8001
│  TextRank NLP Pipeline  │
└─────────────────────────┘
```

| Service | Framework | Role |
|---|---|---|
| `main_app` | Flask | Serves the web UI, accepts user input, relays requests |
| `model_service` | FastAPI | Runs the TextRank pipeline, returns structured summaries |

This separation keeps the NLP logic completely independent of the UI, making each service easy to test, replace, or scale on its own.

---

## 📂 Folder Structure

```
project_exhibition-2/
│
├── main_app/               # Flask web application
│   ├── app.py              # Flask routes and view logic
│   ├── client.py           # HTTP client that calls model_service
│   └── templates/
│       └── index.html      # Frontend UI (form + results display)
│
├── model_service/          # FastAPI NLP service
│   ├── api.py              # POST /summarize endpoint
│   ├── pipeline.py         # Orchestrates the full TextRank pipeline
│   ├── preprocessing.py    # Sentence tokenization and cleaning
│   ├── vectorization.py    # TF-IDF vectorization of sentences
│   ├── similarity.py       # Cosine similarity matrix computation
│   └── ranking.py          # PageRank scoring + top-N extraction
│
├── run.py                  # Starts the Flask app
├── run_model_service.py    # Starts the FastAPI model service
└── requirements.txt        # Python dependencies
```

---

## ⚙️ How the TextRank Pipeline Works

The model service processes text through a **7-step pipeline**, implemented across dedicated modules:

### Step 1 — Sentence Preprocessing (`preprocessing.py`)
The raw input text is split into individual sentences using sentence boundary detection. Each sentence is then cleaned: lowercased, stripped of punctuation, and filtered to remove stopwords (common words like "the", "is", "and" that carry little meaning). This produces a clean token set per sentence, used for comparison.

### Step 2 — TF-IDF Vectorization (`vectorization.py`)
Each sentence is converted into a numerical vector using **TF-IDF** (Term Frequency–Inverse Document Frequency). TF-IDF measures how important a word is to a sentence relative to the entire document — common words score low, distinctive words score high. The output is a matrix where each row is a sentence represented as a weighted word vector.

### Step 3 — Cosine Similarity Matrix (`similarity.py`)
Every sentence vector is compared against every other sentence vector using **cosine similarity**, which measures the angle between two vectors. A score of 1 means identical direction (very similar content), 0 means no overlap. This produces an N×N similarity matrix for N sentences.

### Step 4 — Graph Construction (`ranking.py`)
The similarity matrix is used to build a **weighted undirected graph**, where:
- Each **node** is a sentence
- Each **edge weight** is the cosine similarity between two sentences

Sentences that are semantically similar are strongly connected; unrelated ones have weak or no connection.

### Step 5 — PageRank Scoring (`ranking.py`)
**PageRank** is applied to this graph. Originally designed by Google to rank web pages by how many other pages link to them, here it ranks sentences by how strongly other sentences "endorse" them. A sentence that is similar to many other high-scoring sentences gets a high PageRank score — indicating it captures a central idea of the document.

### Step 6 — Top-N Sentence Extraction (`pipeline.py`)
The top-N sentences (configurable by the user) are selected by their PageRank score.

### Step 7 — Reordering and Final Summary (`pipeline.py`)
Selected sentences are reordered back to their **original position** in the document (not by score), so the output reads naturally and coherently. These sentences are then joined to form the final summary.

---

## 🧰 Technologies Used

| Technology | Purpose |
|---|---|
| **Python** | Primary language for both services |
| **Flask** | Lightweight web framework for the UI server |
| **FastAPI** | High-performance async API framework for the model service |
| **scikit-learn** | TF-IDF vectorization (`TfidfVectorizer`) and cosine similarity |
| **NetworkX** | Graph construction and PageRank computation |
| **NLTK / spaCy** | Sentence tokenization and stopword filtering |
| **NumPy** | Matrix operations on similarity scores |
| **Uvicorn** | ASGI server to run the FastAPI service |
| **Requests** | HTTP client used by Flask to call the model service |

> All summarization is performed locally. No data is sent to any external API.

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8 or higher
- pip

### 1. Clone & Navigate
```bash
git clone <your-repo-url>
cd project_exhibition-2
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. (Optional) Configure Environment
Create a `.env` file in the root directory to override defaults:
```
MODEL_SERVICE_URL=http://127.0.0.1:8001
```
If this file is omitted, the Flask app defaults to `http://127.0.0.1:8001`.

---

## ▶️ Running the Application

You need **two terminals** running simultaneously.

**Terminal 1 — Start the model service (FastAPI):**
```bash
python run_model_service.py
```
The NLP API will be available at `http://127.0.0.1:8001`.

**Terminal 2 — Start the web app (Flask):**
```bash
python run.py
```
The UI will be available at `http://127.0.0.1:5000`.

Open your browser and go to: **http://127.0.0.1:5000**

---

## 🔌 Model Service API Reference

The model service exposes a single endpoint:

### `POST /summarize`

**Request Body (JSON):**
```json
{
  "text": "Paste your full research paper or article text here...",
  "num_sentences": 5
}
```

| Field | Type | Description |
|---|---|---|
| `text` | string | The full input text to be summarized |
| `num_sentences` | integer | Number of top sentences to extract |

**Response (JSON):**
```json
{
  "summary": "The final summary as a single string.",
  "selected_sentences": [
    "Sentence one selected by TextRank.",
    "Sentence two selected by TextRank."
  ],
  "processing_time": 0.1234
}
```

| Field | Type | Description |
|---|---|---|
| `summary` | string | Full summary, sentences joined in document order |
| `selected_sentences` | array of strings | The individual extracted sentences |
| `processing_time` | float | Time taken by the pipeline in seconds |

You can also test the API directly using tools like **curl** or **Postman**:
```bash
curl -X POST http://127.0.0.1:8001/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "Your research text here...", "num_sentences": 3}'
```

---

## 💡 Key Design Decisions

**Why extractive, not abstractive?**
Extractive summarization uses original sentences directly from the text — no language model needed, no hallucination risk, and fully explainable results. Every sentence in the output can be traced back to the source.

**Why two services?**
Splitting the UI and the NLP logic into separate services (microservice pattern) means either can be updated, replaced, or scaled without affecting the other. The Flask UI could be swapped for a React frontend, or the model service could be upgraded to a different algorithm, without rewriting the whole system.

**Why PageRank for sentence ranking?**
PageRank rewards sentences that are broadly similar to many others — these tend to be the most representative and central ideas in the document. It is a well-studied, parameter-light algorithm that works reliably on technical text.

---

## 📌 Limitations

- Works best on **structured, formal text** (research papers, reports, articles). Very informal or conversational text may yield lower quality summaries.
- Purely **extractive**: the summary is always composed of original sentences, never paraphrased or rewritten.
- Very short texts (fewer than ~10 sentences) may not benefit significantly from summarization.
