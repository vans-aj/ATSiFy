import os
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

try:
    from dotenv import load_dotenv
    _ENV_PATH = Path(__file__).resolve().parents[1] / '.env'
    load_dotenv(_ENV_PATH, override=True)
except ImportError:
    pass

#api metadata
APP_TITLE='ATS RESUME ANALYZER API'
APP_VERSION='1.0.0'
APP_DESCRIPTION='analyse resumes against job description using nlp + ml'

ALLOWED_ORIGINS = [
    "https://localhost:5173",
    "http://localhost:3000",
    "https://127.0.0.1:5173",
    "http://127.0.0.1:5500/"
]  

#file 
MAX_FILE_SIZE_MB=5
MAX_FILE_SIZE_BYTES=MAX_FILE_SIZE_MB*1024*1024

#Supported MIME types and their short names
SUPPORTED_MIME_TYPES = {
    'application/pdf': 'pdf',
    'application/msword': 'doc',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
}

SUPPORTED_EXTENSIONS = {'.pdf', '.doc', '.docx'}

SPACY_MODEL_PRIMARY="en_core_web_md" #better accuracy
SPACY_MODEL_SECONDARY="en_core_web_sm" 
SENTENCE_TRANSFORMER_MODEL = os.getenv("SENTENCE_TRANSFORMER_MODEL", "all-MiniLM-L6-v2")

# Score component weights — this is business logic treated as config
SCORE_WEIGHTS = {
    "formatting": 20, "keywords": 25, "content": 25,
    "skill_validation": 15, "ats_compatibility": 15,
}

JD_KEYWORD_WEIGHT=0.6
JD_SEMANTIC_WEIGHT=0.4

def _normalize_supabase_url(url: str) -> str:
    """Return the Supabase project base URL, even if an API path was pasted."""
    if not url:
        return ''

    parts = urlsplit(url.strip())
    path = parts.path.rstrip('/')
    for suffix in ('/rest/v1', '/auth/v1', '/storage/v1'):
        if path == suffix or path.endswith(suffix):
            path = path[: -len(suffix)]
            break

    return urlunsplit((parts.scheme, parts.netloc, path.rstrip('/'), '', ''))


SUPABASE_URL       = _normalize_supabase_url(os.getenv('SUPABASE_URL', ''))
SUPABASE_KEY       = (
    os.getenv('SUPABASE_KEY', '')
    or os.getenv('SUPABASE_SECRET_KEY', '')
)                                                            # service_role — DB writes (bypasses RLS)
SUPABASE_ANON_KEY  = os.getenv('SUPABASE_ANON_KEY', '')      # public anon — frontend auth calls
SUPABASE_JWT_SECRET= os.getenv('SUPABASE_JWT_SECRET', '')    # used by backend to verify access tokens
GROQ_API_KEY       = os.getenv('GROQ_API_KEY', '')
