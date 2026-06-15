from typing import Tuple


def get_score_color(score: float) -> Tuple[str, str]:
    """Return (text_color, background_color) for a 0–100 score."""
    if score >= 80:
        return "#2e7d32", "#e8f5e9"  # green
    if score >= 60:
        return "#f57c00", "#fff3e0"  # orange
    return "#c62828", "#ffebee"      # red


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
        return "High", "#b42318", "#fef3f2"
    if level == "medium":
        return "Medium", "#b54708", "#fffaeb"
    return "Low", "#067647", "#ecfdf3"
