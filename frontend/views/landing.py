import streamlit as st


def render() -> None:
    st.markdown(
        """
        <section class="product-hero">
            <div>
                <p class="eyebrow">Resume intelligence</p>
                <h1>ATS Resume Scorer</h1>
                <p class="hero-copy">
                    Score a resume, compare it with a target job description, and get clear
                    fixes for formatting, keywords, content quality, and skill evidence.
                </p>
            </div>
            <div class="hero-actions">
                <span>Workspace</span>
                <strong>Resume analysis and improvement</strong>
                <p>Run a structured report from one upload.</p>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([0.34, 0.66])
    with left:
        if st.button("Analyze a Resume", use_container_width=True, type="primary"):
            st.session_state.current_view = "scorer"
            st.rerun()
    with right:
        st.caption("Sign in from the sidebar to save analysis history and export reports.")

    st.markdown(
        """
        <div class="stat-grid">
            <div><span class="section-label">Scoring areas</span><strong>5 checks</strong></div>
            <div><span class="section-label">Resume formats</span><strong>PDF / DOC / DOCX</strong></div>
            <div><span class="section-label">Targeting</span><strong>Optional JD match</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("## Core Workflow")
    st.markdown(
        """
        <div class="process-list">
            <div class="feature-card">
                <span class="card-kicker">Step 01</span>
                <h3>Upload</h3>
                <p>Add the resume and, when needed, paste the target job description.</p>
            </div>
            <div class="feature-card">
                <span class="card-kicker">Step 02</span>
                <h3>Analyze</h3>
                <p>Run checks for structure, keywords, skills, content, and ATS compatibility.</p>
            </div>
            <div class="feature-card">
                <span class="card-kicker">Step 03</span>
                <h3>Improve</h3>
                <p>Use prioritized recommendations to update the resume and export the report.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("## What You Get")
    st.markdown(
        """
        <div class="insight-grid">
            <div class="content-card">
                <h3>Structured scoring</h3>
                <p>Breakdowns for formatting, keywords, content, skill validation, and ATS compatibility.</p>
            </div>
            <div class="content-card">
                <h3>Targeted feedback</h3>
                <p>Strengths, critical issues, detailed feedback, and action items for resume edits.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
