import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from backend.core.config import(
    ALLOWED_ORIGINS, 
    APP_DESCRIPTION, 
    APP_TITLE, 
    APP_VERSION, 
    SPACY_MODEL_PRIMARY, 
    SPACY_MODEL_SECONDARY, SENTENCE_TRANSFORMER_MODEL
)

from backend.api.routes import router


logger=logging.getLogger('ats_resume_scorer')

@asynccontextmanager
async def lifespan(app:FastAPI):
    logger.info('Starting ATS Resume Analyzer API...')

    logger.info(f'Loading spaCy NLP model: {SPACY_MODEL_PRIMARY}')
    import spacy
    try:
        app.state.nlp = spacy.load(SPACY_MODEL_PRIMARY)
        logger.info(f'Loaded {SPACY_MODEL_PRIMARY}')
    except OSError:
        logger.warning(f'{SPACY_MODEL_PRIMARY} not found — falling back to {SPACY_MODEL_SECONDARY}')
        app.state.nlp = spacy.load(SPACY_MODEL_SECONDARY)
        logger.info(f'Loaded {SPACY_MODEL_SECONDARY} (fallback)')

    logger.info(f'Loading SentenceTransformer: {SENTENCE_TRANSFORMER_MODEL}')
    from sentence_transformers import SentenceTransformer
    app.state.embedder = SentenceTransformer(SENTENCE_TRANSFORMER_MODEL)
    logger.info(f'Loaded {SENTENCE_TRANSFORMER_MODEL}')

    logger.info('All models loaded. API is ready to serve requests.')

    yield

    logger.info('shutting down the api!!')

app=FastAPI(
    title=APP_TITLE, 
    description=APP_DESCRIPTION, 
    version=APP_VERSION, 
    lifespan=lifespan,
    docs_url='/docs',
    redoc_url='/redoc'
)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True, 
    allow_methods     = ['*'],
    allow_headers     = ['*'],

)

app.include_router(router)



from pathlib import Path as _Path

_FRONTEND_DIR = _Path(__file__).resolve().parent.parent / 'frontend-new'

if _FRONTEND_DIR.is_dir():
    app.mount('/static', StaticFiles(directory=str(_FRONTEND_DIR)), name='static-frontend')

@app.get('/')
async def root(request: Request):
    index = _FRONTEND_DIR / 'index.html'
    if index.is_file():
        from fastapi.responses import FileResponse
        return FileResponse(str(index))
    return {"message": "Welcome to the ATS Resume Analyzer API!"}


@app.get('/analyzer')
@app.get('/history')
@app.get('/resources')
async def serve_page(request: Request):
    from fastapi.responses import FileResponse
    page_name = request.url.path.strip('/')
    page_file = _FRONTEND_DIR / f'{page_name}.html'
    if page_file.is_file():
        return FileResponse(str(page_file))
    return FileResponse(str(_FRONTEND_DIR / 'index.html'))


if __name__=='__main__':
    import uvicorn
    uvicorn.run(
        'backend.main:app',
        host    = '0.0.0.0',
        port    = 8000,
        reload  = True,    # Auto-restart on code changes (dev only)
    )