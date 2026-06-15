import io
import logging
import os
from pathlib import Path

try:
    homebrew_lib = Path("/opt/homebrew/lib")
    if homebrew_lib.exists():
        existing = os.environ.get("DYLD_LIBRARY_PATH", "")
        paths = [str(homebrew_lib)]
        if existing:
            paths.append(existing)
        os.environ["DYLD_LIBRARY_PATH"] = ":".join(paths)

    from weasyprint import HTML, CSS
    WEASYPRINT_INSTALLED = True
    WEASYPRINT_IMPORT_ERROR = None
except Exception as exc:
    WEASYPRINT_INSTALLED = False
    WEASYPRINT_IMPORT_ERROR = exc

logger = logging.getLogger('ats_resume_scorer')

def generate_combined_pdf(html_docs: dict[str, str]) -> bytes:
    if not WEASYPRINT_INSTALLED:
        raise RuntimeError(
            "PDF generation unavailable. WeasyPrint could not load its native dependencies. "
            f"Original error: {WEASYPRINT_IMPORT_ERROR}"
        )
        
    documents = []
    
    # Render all 3 HTML strings to WeasyPrint Document objects
    for name, html_str in html_docs.items():
        doc = HTML(string=html_str).render()
        documents.append(doc)
    
    # Merge them into the first document
    first_doc = documents[0]
    for other_doc in documents[1:]:
        for page in other_doc.pages:
            first_doc.pages.append(page)
            
    # Write combined PDF bytes
    pdf_bytes = first_doc.write_pdf()
    return pdf_bytes
