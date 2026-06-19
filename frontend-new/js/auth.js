// Auth module – wraps Supabase client for sign-in / sign-up / OAuth / sign-out
import CONFIG from './config.js';

let supabaseClient = null;

function getClient() {
  if (supabaseClient) return supabaseClient;
  if (!CONFIG.SUPABASE_URL || !CONFIG.SUPABASE_ANON_KEY) return null;
  // supabase-js is loaded via CDN in the HTML
  supabaseClient = window.supabase.createClient(CONFIG.SUPABASE_URL, CONFIG.SUPABASE_ANON_KEY);
  return supabaseClient;
}

// ---------- state helpers ----------
const STATE_KEY = 'atsify_auth';

export function getAuth() {
  try {
    return JSON.parse(localStorage.getItem(STATE_KEY)) || null;
  } catch { return null; }
}

export function setAuth(data) {
  localStorage.setItem(STATE_KEY, JSON.stringify(data));
  window.dispatchEvent(new CustomEvent('auth-changed', { detail: data }));
}

export function clearAuth() {
  localStorage.removeItem(STATE_KEY);
  window.dispatchEvent(new CustomEvent('auth-changed', { detail: null }));
}

export function isLoggedIn() { return !!getAuth()?.access_token; }

// ---------- sign-in ----------
export async function signInWithPassword(email, password) {
  const client = getClient();
  if (!client) return { error: 'Supabase not configured' };
  try {
    const { data, error } = await client.auth.signInWithPassword({ email, password });
    if (error) return { error: _humanize(error.message) };
    const session = data.session;
    const user = data.user;
    const auth = {
      access_token: session.access_token,
      refresh_token: session.refresh_token,
      user_id: user.id,
      email: user.email,
    };
    setAuth(auth);
    return auth;
  } catch (e) {
    return { error: e.message };
  }
}

// ---------- sign-up ----------
export async function signUpWithPassword(email, password) {
  const client = getClient();
  if (!client) return { error: 'Supabase not configured' };
  try {
    const { data, error } = await client.auth.signUp({
      email,
      password,
      options: { emailRedirectTo: CONFIG.OAUTH_REDIRECT },
    });
    if (error) return { error: _humanize(error.message) };
    if (data.session && data.user) {
      const auth = {
        access_token: data.session.access_token,
        refresh_token: data.session.refresh_token,
        user_id: data.user.id,
        email: data.user.email,
      };
      setAuth(auth);
      return auth;
    }
    if (data.user) return { pending_confirmation: true, email };
    return { error: 'Sign-up failed' };
  } catch (e) {
    return { error: e.message };
  }
}

// ---------- Google OAuth ----------
export async function googleOAuthUrl() {
  const client = getClient();
  if (!client) return { error: 'Supabase not configured' };
  try {
    const { data, error } = await client.auth.signInWithOAuth({
      provider: 'google',
      options: { redirectTo: CONFIG.OAUTH_REDIRECT },
    });
    if (error) return { error: error.message };
    return { url: data.url };
  } catch (e) {
    return { error: e.message };
  }
}

// ---------- exchange code (OAuth callback) ----------
export async function exchangeCodeForSession(code) {
  const client = getClient();
  if (!client) return { error: 'Supabase not configured' };
  try {
    const { data, error } = await client.auth.exchangeCodeForSession(code);
    if (error) return { error: error.message };
    const session = data.session;
    const user = data.user;
    if (!session || !user) return { error: 'OAuth exchange returned no session' };
    const auth = {
      access_token: session.access_token,
      refresh_token: session.refresh_token,
      user_id: user.id,
      email: user.email,
    };
    setAuth(auth);
    return auth;
  } catch (e) {
    return { error: e.message };
  }
}

// ---------- sign-out ----------
export async function signOut() {
  const client = getClient();
  if (client) {
    try { await client.auth.signOut(); } catch {}
  }
  clearAuth();
}

// ---------- helpers ----------
function _humanize(msg) {
  const m = msg.toLowerCase();
  if (m.includes('invalid login') || m.includes('invalid_grant')) return 'Wrong email or password';
  if (m.includes('already registered') || m.includes('already been registered')) return 'An account with this email already exists. Try signing in';
  if (m.includes('password should be at least')) return 'Password too short (minimum 6 characters)';
  return msg;
}

// On load, check for OAuth callback code in URL
export function handleOAuthCallback() {
  const params = new URLSearchParams(window.location.search);
  const code = params.get('code');
  if (code && !isLoggedIn()) {
    exchangeCodeForSession(code).then(result => {
      // Clear URL params
      window.history.replaceState({}, '', window.location.pathname);
      if (!result.error) {
        window.location.reload();
      }
    });
  }
}
