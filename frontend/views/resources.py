import streamlit as st


def render():
    """Render the resources page"""
    
    st.markdown(
        """
        <div class="page-heading">
            <p class="eyebrow">Reference</p>
            <h1>Resources and Tips</h1>
            <p>Practical guidance for building resumes that parse cleanly and match target roles.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown("## ATS Optimization Tips")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            """
            <div class="content-card">
                <h3>Recommended</h3>
                <ul>
                    <li>Use standard section headings</li>
                    <li>Include relevant keywords from the job description</li>
                    <li>Use simple, clean formatting</li>
                    <li>List skills explicitly</li>
                    <li>Quantify achievements with numbers</li>
                    <li>Use standard fonts such as Arial, Calibri, or Times New Roman</li>
                    <li>Save as PDF or DOCX</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col2:
        st.markdown(
            """
            <div class="content-card">
                <h3>Avoid</h3>
                <ul>
                    <li>Tables and text boxes</li>
                    <li>Headers or footers for important information</li>
                    <li>Images and graphics for core content</li>
                    <li>Unusual fonts</li>
                    <li>Multi-column layouts for critical sections</li>
                    <li>Keyword stuffing</li>
                    <li>Abbreviations without spelling them out first</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    st.markdown("---")
    
    st.markdown("## Common ATS Keywords by Industry")
    
    tab1, tab2, tab3 = st.tabs(["Technology", "Business", "Creative"])
    
    with tab1:
        st.markdown("""
        **Software Development:**
        - Programming languages (Python, Java, JavaScript)
        - Frameworks (React, Django, Spring)
        - Tools (Git, Docker, Kubernetes)
        - Methodologies (Agile, Scrum, CI/CD)
        """)
    
    with tab2:
        st.markdown("""
        **Business & Management:**
        - Project management
        - Stakeholder engagement
        - Budget management
        - Strategic planning
        - Team leadership
        """)
    
    with tab3:
        st.markdown("""
        **Creative & Design:**
        - Adobe Creative Suite
        - UI/UX Design
        - Wireframing & Prototyping
        - Brand identity
        - Visual communication
        """)
    
    st.markdown("---")
    
    st.markdown("## ATS-Friendly Resume Templates")
    st.info("Coming soon: Downloadable ATS-optimized resume templates")
