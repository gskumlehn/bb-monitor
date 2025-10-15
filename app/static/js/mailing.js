// Usa as rotas injetadas pelo template. Garante barra final pra evitar 308.
const GET_URL  = (window.API_GET  || '/mailing/');
const POST_URL = (window.API_POST || '/mailing/');
const DEL_URL  = (window.API_DEL  || '/mailing/');

// DOM
const addForm = document.getElementById('addForm');
const emailInput = document.getElementById('email');
const directorateCodeInput = document.getElementById('directorate_code');
const submitBtn = document.getElementById('submitBtn');
const emailList = document.getElementById('emailList');
const emailCount = document.getElementById('emailCount');
const toast = document.getElementById('toast');

// State
let entries = [];
let isLoading = false;

// Init
document.addEventListener('DOMContentLoaded', () => {
  loadEntries();
  addForm?.addEventListener('submit', handleSubmit);
});

// API — GET lista
async function loadEntries() {
  try {
    const res = await fetch(GET_URL, { method: 'GET', credentials: 'same-origin' });
    if (!res.ok) throw new Error(`GET ${GET_URL} => ${res.status}`);
    entries = await res.json();
    renderList();
  } catch (err) {
    console.error(err);
    showToast('Erro ao carregar lista de e-mails', 'error');
  }
}

// API — POST add
async function handleSubmit(e) {
  e.preventDefault();

  const email = emailInput.value.trim();
  const directorate_code = directorateCodeInput.value.trim();

  if (!email || !directorate_code) {
    showToast('Preencha todos os campos', 'error');
    return;
  }
  if (isLoading) return;

  isLoading = true;
  submitBtn.disabled = true;
  const original = submitBtn.innerHTML;
  submitBtn.textContent = 'Adicionando...';

  try {
    const res = await fetch(POST_URL, {
      method: 'POST',
      credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, directorate_code }),
    });

    if (!res.ok) {
      let msg = 'Erro ao adicionar e-mail';
      try {
        const data = await res.json();
        if (data?.error) msg = data.error;
      } catch {}
      throw new Error(msg);
    }

    showToast('E-mail adicionado com sucesso!', 'success');
    addForm.reset();
    await loadEntries();
  } catch (err) {
    console.error(err);
    showToast(err.message || 'Erro ao adicionar e-mail', 'error');
  } finally {
    isLoading = false;
    submitBtn.disabled = false;
    submitBtn.innerHTML = original;
  }
}

// API — DELETE
async function handleDelete(email, directorate_code) {
  if (!confirm('Tem certeza que deseja remover este e-mail?')) return;

  try {
    const params = new URLSearchParams({ email, directorate_code });
    const url = `${DEL_URL}?${params.toString()}`;

    const res = await fetch(url, {
      method: 'DELETE',
      credentials: 'same-origin',
    });

    if (!res.ok) throw new Error(`Erro ao remover e-mail (${res.status})`);

    showToast('E-mail removido com sucesso!', 'success');
    await loadEntries();
  } catch (err) {
    console.error(err);
    showToast('Erro ao remover e-mail', 'error');
  }
}

// Render
function renderList() {
  emailCount.textContent = entries.length;

  if (!entries.length) {
    emailList.innerHTML = `
      <div class="empty-state">
        <svg class="empty-icon" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
          <rect x="2" y="4" width="20" height="16" rx="2"></rect>
          <path d="m2 7 10 7 10-7"></path>
        </svg>
        <p>Nenhum e-mail cadastrado ainda</p>
      </div>
    `;
    return;
  }

  emailList.innerHTML = entries.map(entry => `
    <div class="email-item">
      <div class="email-info">
        <div class="email-text">
          <svg class="icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
            <rect x="2" y="4" width="20" height="16" rx="2"></rect>
            <path d="m2 7 10 7 10-7"></path>
          </svg>
          ${escapeHtml(entry.email)}
        </div>
        <div class="code-text">
          <svg class="icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
            <polyline points="9 22 9 12 15 12 15 22"></polyline>
          </svg>
          ${escapeHtml(entry.directorate_code)}
        </div>
      </div>
      <button
        class="btn-delete"
        onclick="handleDelete('${escapeAttr(entry.email)}', '${escapeAttr(entry.directorate_code)}')"
        title="Remover"
        aria-label="Remover ${escapeAttr(entry.email)} (${escapeAttr(entry.directorate_code)})">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
          <polyline points="3 6 5 6 21 6"></polyline>
          <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
        </svg>
      </button>
    </div>
  `).join('');
}

// Toast
function showToast(message, type = 'success') {
  toast.textContent = message;
  toast.className = `toast ${type} show`;
  setTimeout(() => toast.classList.remove('show'), 3000);
}

// Helpers
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = String(text ?? '');
  return div.innerHTML;
}
function escapeAttr(text) {
  // mais estrito para atributos inline
  return String(text ?? '').replace(/['"<>&]/g, c => ({
    "'":"&#39;", '"':"&quot;", "<":"&lt;", ">":"&gt;", "&":"&amp;",
  }[c]));
}

// expõe delete no escopo global (usado no onclick do template)
window.handleDelete = handleDelete;
