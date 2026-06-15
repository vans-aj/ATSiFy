import streamlit as st


def render() -> None:
    st.markdown(
        """
        <section class="hero-shell">
            <div>
                <p class="eyebrow">Resume intelligence</p>
                <h1>Score, compare, and improve resumes with a focused ATS workflow.</h1>
                <p class="hero-copy">
                    Upload a resume, run structured checks, compare against a job description,
                    and keep past analyses tied to your account.
                </p>
            </div>
            <div class="hero-panel">
                <span>Current workspace</span>
                <strong>ATS Resume Scorer</strong>
                <p>Formatting, keyword coverage, content quality, skill evidence, and compatibility in one report.</p>
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
        <div class="metric-strip">
            <div><span>Scoring areas</span><strong>5</strong></div>
            <div><span>Resume formats</span><strong>PDF / DOC / DOCX</strong></div>
            <div><span>Optional comparison</span><strong>Job description match</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("## Core Workflow")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <span class="card-kicker">Step 01</span>
                <h3>Upload</h3>
                <p>Add the resume file and optionally paste a target job description.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <span class="card-kicker">Step 02</span>
                <h3>Analyze</h3>
                <p>Run checks for structure, keyword alignment, skills, and ATS compatibility.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <span class="card-kicker">Step 03</span>
                <h3>Improve</h3>
                <p>Review prioritized recommendations, export reports, and track saved history.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("## What You Get")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            <div class="content-card">
                <h3>Structured scoring</h3>
                <p>Breakdowns for formatting, keywords, content, skill validation, and ATS compatibility.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="content-card">
                <h3>Targeted feedback</h3>
                <p>Clear strengths, critical issues, detailed feedback, and action items for resume edits.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
