// app/static/js/mailing.js

// Base dinâmico: sempre HTTPS no mesmo host/porta/rota
const API_BASE = `${window.location.origin}/mailing`;

// DOM Elements
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

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  loadEntries();
  addForm.addEventListener('submit', handleSubmit);
});

// Load all entries
async function loadEntries() {
  try {
    const url = `${API_BASE}`;
    const response = await fetch(url, { method: 'GET' });
    if (!response.ok) throw new Error(`GET /mailing => ${response.status}`);

    entries = await response.json();
    renderList();
  } catch (error) {
    showToast('Erro ao carregar lista de e-mails', 'error');
    console.error(error);
  }
}

// Handle form submission
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
  submitBtn.textContent = 'Adicionando...';

  try {
    const response = await fetch(`${API_BASE}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, directorate_code }),
    });

    if (response.ok) {
      showToast('E-mail adicionado com sucesso!', 'success');
      emailInput.value = '';
      directorateCodeInput.value = '';
      await loadEntries();
    } else {
      const error = await safeJson(response);
      showToast(error.error || 'Erro ao adicionar e-mail', 'error');
      throw new Error(`POST /mailing => ${response.status}`);
    }
  } catch (error) {
    console.error(error);
  } finally {
    isLoading = false;
    submitBtn.disabled = false;
    submitBtn.innerHTML = `
      <svg class="icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <line x1="12" y1="5" x2="12" y2="19"></line>
        <line x1="5" y1="12" x2="19" y2="12"></line>
      </svg>
      Adicionar à Lista
    `;
  }
}

// Delete entry
async function handleDelete(email, directorate_code) {
  if (!confirm('Tem certeza que deseja remover este e-mail?')) return;

  try {
    const params = new URLSearchParams({ email, directorate_code });
    const response = await fetch(`${API_BASE}?${params.toString()}`, { method: 'DELETE' });

    if (response.ok) {
      showToast('E-mail removido com sucesso!', 'success');
      await loadEntries();
    } else {
      const error = await safeJson(response);
      showToast(error.error || 'Erro ao remover e-mail', 'error');
      throw new Error(`DELETE /mailing => ${response.status}`);
    }
  } catch (error) {
    console.error(error);
  }
}

// Helpers
async function safeJson(res) {
  try { return await res.json(); } catch { return {}; }
}

function renderList() {
  emailCount.textContent = entries.length;

  if (entries.length === 0) {
    emailList.innerHTML = `
      <div class="empty-state">
        <svg class="empty-icon" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="2" y="4" width="20" height="16" rx="2"></rect>
          <path d="m2 7 10 7 10-7"></path>
        </svg>
        <p>Nenhum e-mail cadastrado ainda</p>
      </div>
    `;
    return;
  }

  const html = entries.map(entry => `
    <div class="email-item">
      <div class="email-info">
        <div class="email-text">
          <svg class="icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="2" y="4" width="20" height="16" rx="2"></rect>
            <path d="m2 7 10 7 10-7"></path>
          </svg>
          ${escapeHtml(entry.email)}
        </div>
        <div class="code-text">
          <svg class="icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
            <polyline points="9 22 9 12 15 12 15 22"></polyline>
          </svg>
          ${escapeHtml(entry.directorate_code)}
        </div>
      </div>
      <button
        class="btn-delete"
        onclick="handleDelete('${escapeHtml(entry.email)}', '${escapeHtml(entry.directorate_code)}')"
        title="Remover"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="3 6 5 6 21 6"></polyline>
          <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
        </svg>
      </button>
    </div>
  `).join('');

  emailList.innerHTML = html;
}

function showToast(message, type = 'success') {
  toast.textContent = message;
  toast.className = `toast ${type} show`;
  setTimeout(() => toast.classList.remove('show'), 3000);
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// Expose
window.handleDelete = handleDelete;
