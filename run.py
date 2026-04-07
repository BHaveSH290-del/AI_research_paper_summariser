#!/usr/bin/env python3
"""Run Flask main application."""
from main_app.app import app


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
