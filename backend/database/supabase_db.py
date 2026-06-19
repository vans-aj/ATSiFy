#This file’s entire job is:

#1. Save an ATS analysis result into Supabase.
#2. Fetch all previous analyses of a user.
#3. Delete an analysis.


import logging
import httpx
import json
from datetime import datetime, timezone
from typing import List, Optional, Dict

logger = logging.getLogger('ats_resume_scorer')

from backend.core.config import SUPABASE_URL, SUPABASE_KEY

def _get_headers():
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

async def save_analysis(user_id: str, filename: str, analysis_result: Dict) -> Optional[str]:
    headers = _get_headers()
    if not headers:
        logger.warning("save_analysis skipped: SUPABASE_URL or SUPABASE_KEY not configured")
        return None

    def _json_default(o):
        if hasattr(o, 'model_dump'):
            return o.model_dump()
        return str(o)
    serializable_result = json.loads(json.dumps(analysis_result, default=_json_default))

    doc = {
        "user_id": user_id,
        "filename": filename,
        "ats_score": serializable_result.get("ats_score", 0),
        "keyword_match": serializable_result.get("keyword_match", 0),
        "missing_keywords": serializable_result.get("missing_keywords", []),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "analysis_result": serializable_result,
    }

    url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/analyses"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=doc)
            response.raise_for_status()
            data = response.json()
            if data and len(data) > 0:
                inserted_id = str(data[0].get("id"))
                logger.info(f"Saved analysis for user {user_id}: {inserted_id}")
                return inserted_id
            return None
    except Exception as exc:
        logger.error(f"Failed to save analysis to Supabase: {exc}")
        return None

async def get_user_history(user_id: str) -> List[Dict]:
    headers = _get_headers()
    if not headers:
        raise RuntimeError("Cannot fetch history: SUPABASE_URL or SUPABASE_KEY not configured")

    url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/analyses"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers=headers,
            params={
                "user_id": f"eq.{user_id}",
                "order": "created_at.desc"
            }
        )
        response.raise_for_status()
        docs = response.json()

        results = []
        for doc in docs:
            results.append({
                "id": str(doc.get("id")),
                "filename": doc.get("filename", "resume"),
                "resume_name": doc.get("filename", "resume"),
                "job_title": "Software Engineer",
                "ats_score": doc.get("ats_score", 0),
                "keyword_match": doc.get("keyword_match", 0),
                "missing_keywords": doc.get("missing_keywords", []),
                "date": doc.get("created_at", ""),
                "created_at": doc.get("created_at", ""),
                "analysis_result": doc.get("analysis_result", {}),
            })
        return results

async def delete_analysis(analysis_id: str, user_id: str) -> bool:
    headers = _get_headers()
    if not headers:
        raise RuntimeError("Cannot delete analysis: SUPABASE_URL or SUPABASE_KEY not configured")

    url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/analyses"

    async with httpx.AsyncClient() as client:
        response = await client.delete(
            url,
            headers=headers,
            params={
                "id": f"eq.{analysis_id}",
                "user_id": f"eq.{user_id}"
            }
        )
        response.raise_for_status()
        return True