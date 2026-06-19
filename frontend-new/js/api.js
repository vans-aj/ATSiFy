// API client – all backend calls go through here
import CONFIG from './config.js';
import { getAuth } from './auth.js';

function _headers() {
  const auth = getAuth();
  const h = { 'Accept': 'application/json' };
  if (auth?.access_token) h['Authorization'] = `Bearer ${auth.access_token}`;
  return h;
}

function _url(path) {
  return `${CONFIG.BACKEND_URL}${path}`;
}

export async function healthCheck() {
  const res = await fetch(_url('/api/v1/health'), { headers: _headers(), signal: AbortSignal.timeout(10000) });
  if (!res.ok) throw new Error(`Health check failed: ${res.status}`);
  return res.json();
}

export async function analyzeResume(resumeFile, jobDescription = '') {
  const fd = new FormData();
  fd.append('resume', resumeFile);
  fd.append('job_description', jobDescription);

  const auth = getAuth();
  const h = {};
  if (auth?.access_token) h['Authorization'] = `Bearer ${auth.access_token}`;

  const res = await fetch(_url('/api/v1/analyze-resume'), {
    method: 'POST',
    headers: h,
    body: fd,
    signal: AbortSignal.timeout(180000),
  });
  if (!res.ok) {
    const body = await res.text();
    let detail = body;
    try { detail = JSON.parse(body).detail || body; } catch {}
    throw new Error(`${res.status}: ${detail}`);
  }
  return res.json();
}

export async function getHistory() {
  const res = await fetch(_url('/api/v1/history'), { headers: _headers(), signal: AbortSignal.timeout(30000) });
  if (!res.ok) throw new Error(`Failed to load history: ${res.status}`);
  return res.json();
}

export async function deleteHistoryEntry(analysisId) {
  const res = await fetch(_url(`/api/v1/history/${analysisId}`), {
    method: 'DELETE',
    headers: _headers(),
    signal: AbortSignal.timeout(30000),
  });
  if (!res.ok) throw new Error(`Failed to delete: ${res.status}`);
  return res.json();
}

export async function generatePdf(analysisData) {
  const auth = getAuth();
  const h = { 'Content-Type': 'application/json' };
  if (auth?.access_token) h['Authorization'] = `Bearer ${auth.access_token}`;

  const res = await fetch(_url('/api/v1/generate-pdf'), {
    method: 'POST',
    headers: h,
    body: JSON.stringify(analysisData),
    signal: AbortSignal.timeout(60000),
  });
  if (!res.ok) throw new Error(`PDF generation failed: ${res.status}`);
  return res.blob();
}

export async function getHistoryPdf(analysisId) {
  const res = await fetch(_url(`/api/v1/history/${analysisId}/pdf`), {
    headers: _headers(),
    signal: AbortSignal.timeout(60000),
  });
  if (!res.ok) throw new Error(`PDF download failed: ${res.status}`);
  return res.blob();
}
