from typing import Tuple


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
