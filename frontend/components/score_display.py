from typing import Any, Dict

import streamlit as st

from frontend.components._helpers import get_score_color, get_score_label


# Component max scores match backend/core/config.py SCORE_WEIGHTS.
# (Backend returns each component's score on its own scale, not 0–100.)
COMPONENTS = [
    ("Formatting",        "formatting",        20),
    ("Keywords & Skills", "keywords",          25),
    ("Content Quality",   "content",           25),
    ("Skill Validation",  "skill_validation",  15),
    ("ATS Compatibility", "ats_compatibility", 15),
]


def display_overall_score(analysis: Dict[str, Any]) -> None:
    """Big colored score card with a short interpretation line."""
    score = float(analysis.get("ATS_score", analysis.get("ats_score", 0)))
    interpretation = analysis.get("interpretation", "")
    text_color, score_class = get_score_color(score)
    score_label = get_score_label(score)

    st.markdown("## Analysis Results")
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown(
            f"""
            <div class="score-panel {score_class}">
                <p class="score-label" style="color:{text_color};">{score_label}</p>
                <h1 style="color:{text_color};">
                    {score:.0f}
                </h1>
                <h3 style="color:{text_color};">Overall ATS Score</h3>
                <p>{interpretation}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def display_score_breakdown(analysis: Dict[str, Any]) -> None:
    """Five progress bars, one per scoring component."""
    component_scores = analysis.get("component_scores") or {}
    st.markdown("### Score Breakdown")

    left, right = st.columns(2)
    for i, (label, key, max_score) in enumerate(COMPONENTS):
        value = float(component_scores.get(key, 0))
        percentage = value / max_score if max_score else 0
        bar_class = "good" if percentage >= 0.8 else "mid" if percentage >= 0.6 else "low"
        width = min(max(percentage * 100, 0), 100)

        with left if i % 2 == 0 else right:
            st.markdown(
                f"""
                <div class="score-row">
                    <strong>{label}</strong>
                    <div class="progress-track">
                        <div class="progress-fill {bar_class}" style="width:{width:.0f}%;"></div>
                    </div>
                    <span>{value:.0f}/{max_score}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
