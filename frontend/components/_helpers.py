from typing import Tuple

import requests
import streamlit as st


def show_backend_error(exc: Exception) -> None:
    if isinstance(exc, requests.ConnectionError):
        st.error("Could not reach the backend. Is `uvicorn backend.main:app` running on port 8000?")
    elif isinstance(exc, requests.Timeout):
        st.error("The backend took too long to respond. Try a smaller resume or check the server logs.")
    elif isinstance(exc, requests.HTTPError) and exc.response is not None:
        try:
            detail = exc.response.json().get("detail", exc.response.text)
        except ValueError:
            detail = exc.response.text
        st.error(f"Backend returned {exc.response.status_code}: {detail}")
    else:
        st.error(f"Unexpected error: {exc}")


def get_score_color(score: float) -> Tuple[str, str]:
    """Return (text_color, background_color) for a 0–100 score."""
    if score >= 80:
        return "#34d399", "score-good"
    if score >= 60:
        return "#fbbf24", "score-mid"
    return "#fb7185", "score-low"


def get_score_label(score: float) -> str:
    """Text label that matches the score band."""
    if score >= 90:
        return "Excellent"
    if score >= 80:
        return "Strong"
    if score >= 70:
        return "Good"
    if score >= 60:
        return "Needs Work"
    return "High Priority"


def get_severity_style(severity: str) -> Tuple[str, str, str]:
    """
    Return (label, text_color, background_color) for an IssueDetail severity.
    Matches the values the backend emits in `detailed_feedback[].severity_level`.
    """
    level = (severity or "").lower()
    if level in ("critical", "high"):
        return "High", "#fb7185", "issue-high"
    if level == "medium":
        return "Medium", "#fbbf24", "issue-medium"
    return "Low", "#34d399", "issue-low"
