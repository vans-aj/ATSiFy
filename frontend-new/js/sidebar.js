// Sidebar rendering + auth UI
import {
  getAuth, isLoggedIn, signInWithPassword, signUpWithPassword,
  googleOAuthUrl, signOut, handleOAuthCallback,
} from './auth.js';

const NAV_ITEMS = [
  { label: 'Home',      href: '/static/index.html',      icon: '&#9679;' },
  { label: 'Analyze',   href: '/static/analyzer.html',   icon: '&#9670;' },
  { label: 'History',   href: '/static/history.html',    icon: '&#9636;' },
  { label: 'Resources', href: '/static/resources.html',  icon: '&#9733;' },
];

export function initSidebar() {
  handleOAuthCallback();
  renderSidebar();
  window.addEventListener('auth-changed', renderSidebar);
}

function currentPage() {
  const p = window.location.pathname;
  return NAV_ITEMS.find(n => p.endsWith(n.href.split('/').pop())) || NAV_ITEMS[0];
}

function renderSidebar() {
  const sidebar = document.getElementById('sidebar');
  if (!sidebar) return;

  const current = currentPage();

  sidebar.innerHTML = `
    <div class="sidebar-brand">
      <div class="brand-mark">ATS</div>
      <div>
        <h2>ATSiFy</h2>
        <p>Resume Scorer</p>
      </div>
    </div>

    <nav class="sidebar-nav">
      ${NAV_ITEMS.map(n => `
        <a href="${n.href}" class="${n === current ? 'active' : ''}">
          <span class="nav-icon">${n.icon}</span>
          ${n.label}
        </a>
      `).join('')}
    </nav>

    <div class="sidebar-divider"></div>
    <div class="sidebar-section-title">Account</div>
    <div id="auth-section"></div>
  `;

  renderAuthSection();
  setupMobileToggle();
}

function renderAuthSection() {
  const el = document.getElementById('auth-section');
  if (!el) return;

  if (isLoggedIn()) {
    const auth = getAuth();
    const initial = (auth.email || '?')[0].toUpperCase();
    el.innerHTML = `
      <div class="user-badge">
        <div class="avatar">${initial}</div>
        <div class="email">${auth.email}</div>
      </div>
      <button class="btn btn-block btn-sm" id="btn-signout">Sign out</button>
    `;
    document.getElementById('btn-signout').addEventListener('click', async () => {
      await signOut();
      window.location.reload();
    });
  } else {
    el.innerHTML = `
      <div class="auth-tabs">
        <button class="auth-tab active" data-tab="signin">Sign in</button>
        <button class="auth-tab" data-tab="signup">Sign up</button>
      </div>

      <div id="auth-signin" class="auth-form">
        <label>Email</label>
        <input type="email" id="signin-email" placeholder="you@example.com" />
        <label>Password</label>
        <input type="password" id="signin-pw" placeholder="Password" />
        <button class="btn btn-primary btn-block btn-sm" id="btn-signin">Sign in</button>
      </div>

      <div id="auth-signup" class="auth-form hidden">
        <label>Email</label>
        <input type="email" id="signup-email" placeholder="you@example.com" />
        <label>Password (min 6 chars)</label>
        <input type="password" id="signup-pw" placeholder="Password" />
        <button class="btn btn-primary btn-block btn-sm" id="btn-signup">Create account</button>
      </div>

      <div class="auth-divider-text">or</div>
      <button class="btn btn-google btn-block btn-sm" id="btn-google">Continue with Google</button>

      <div id="auth-msg" class="hidden" style="margin-top:.5rem;"></div>
    `;

    // Tab switching
    el.querySelectorAll('.auth-tab').forEach(tab => {
      tab.addEventListener('click', () => {
        el.querySelectorAll('.auth-tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        const target = tab.dataset.tab;
        document.getElementById('auth-signin').classList.toggle('hidden', target !== 'signin');
        document.getElementById('auth-signup').classList.toggle('hidden', target !== 'signup');
      });
    });

    // Sign in
    document.getElementById('btn-signin').addEventListener('click', async () => {
      const email = document.getElementById('signin-email').value;
      const pw = document.getElementById('signin-pw').value;
      if (!email || !pw) return showAuthMsg('Please enter email and password', 'warning');
      showAuthMsg('Signing in...', 'info');
      const result = await signInWithPassword(email, pw);
      if (result.error) return showAuthMsg(result.error, 'error');
      window.location.reload();
    });

    // Sign up
    document.getElementById('btn-signup').addEventListener('click', async () => {
      const email = document.getElementById('signup-email').value;
      const pw = document.getElementById('signup-pw').value;
      if (!email || !pw) return showAuthMsg('Please enter email and password', 'warning');
      showAuthMsg('Creating account...', 'info');
      const result = await signUpWithPassword(email, pw);
      if (result.error) return showAuthMsg(result.error, 'error');
      if (result.pending_confirmation) return showAuthMsg(`Check your inbox. Confirmation sent to ${result.email}`, 'success');
      window.location.reload();
    });

    // Google OAuth
    document.getElementById('btn-google').addEventListener('click', async () => {
      const result = await googleOAuthUrl();
      if (result.error) return showAuthMsg(result.error, 'error');
      if (result.url) window.location.href = result.url;
    });
  }
}

function showAuthMsg(msg, type = 'info') {
  const el = document.getElementById('auth-msg');
  if (!el) return;
  el.className = `alert alert-${type}`;
  el.textContent = msg;
  el.classList.remove('hidden');
}

function setupMobileToggle() {
  const toggle = document.getElementById('sidebar-toggle');
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebar-overlay');
  if (!toggle || !sidebar) return;

  toggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
    overlay?.classList.toggle('visible');
  });
  overlay?.addEventListener('click', () => {
    sidebar.classList.remove('open');
    overlay.classList.remove('visible');
  });
}
