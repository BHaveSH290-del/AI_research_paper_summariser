"""Flask app that calls local model service."""
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, render_template, request

from main_app.client import summarize_via_model_service
from main_app.pdf_reader import extract_text_from_pdf_bytes

load_dotenv()

app = Flask(
    __name__,
    template_folder=str(Path(__file__).resolve().parent / "templates"),
)


@app.get("/")
def index():
    return render_template("index.html", result=None, error=None)


@app.post("/summarize")
def summarize():
    text = (request.form.get("text") or "").strip()
    num_sentences_raw = request.form.get("num_sentences", "5").strip()
    uploaded_file = request.files.get("pdf_file")

    try:
        num_sentences = int(num_sentences_raw)
    except ValueError:
        return render_template(
            "index.html",
            error="Number of sentences must be an integer.",
            result=None,
            original_text=text,
            num_sentences=5,
        )

    if uploaded_file and uploaded_file.filename:
        filename = uploaded_file.filename.lower()
        if not filename.endswith(".pdf"):
            return render_template(
                "index.html",
                error="Only PDF files are allowed.",
                result=None,
                original_text=text,
                num_sentences=num_sentences,
            )
        try:
            file_bytes = uploaded_file.read()
            extracted = extract_text_from_pdf_bytes(file_bytes)
        except Exception as exc:
            return render_template(
                "index.html",
                error=f"Could not read PDF: {exc}",
                result=None,
                original_text=text,
                num_sentences=num_sentences,
            )
        if not extracted:
            return render_template(
                "index.html",
                error="No readable text found in PDF.",
                result=None,
                original_text=text,
                num_sentences=num_sentences,
            )
        text = extracted

    if not text:
        return render_template(
            "index.html",
            error="Please upload a PDF or provide research text.",
            result=None,
            original_text=text,
            num_sentences=num_sentences,
        )

    if num_sentences < 1 or num_sentences > 20:
        return render_template(
            "index.html",
            error="Number of sentences must be between 1 and 20.",
            result=None,
            original_text=text,
            num_sentences=num_sentences,
        )

    try:
        result = summarize_via_model_service(text=text, num_sentences=num_sentences)
    except Exception as exc:
        return render_template(
            "index.html",
            error=f"Model service error: {exc}",
            result=None,
            original_text=text,
            num_sentences=num_sentences,
        )

    return render_template(
        "index.html",
        result=result,
        error=None,
        original_text=text,
        num_sentences=num_sentences,
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.getenv("MAIN_APP_PORT", "5000")), debug=True)
