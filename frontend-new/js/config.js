// Central config – reads from env or falls back to defaults
const CONFIG = {
  BACKEND_URL: window.__BACKEND_URL || 'http://localhost:8000',
  SUPABASE_URL: window.__SUPABASE_URL || '',
  SUPABASE_ANON_KEY: window.__SUPABASE_ANON_KEY || '',
  OAUTH_REDIRECT: window.__OAUTH_REDIRECT || window.location.origin,
};

export default CONFIG;
