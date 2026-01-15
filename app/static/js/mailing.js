// API Base URL
const API_BASE = '/mailing';

// DOM Elements
const saveForm = document.getElementById('saveForm');
const emailInput = document.getElementById('email');
const directorateCodeInput = document.getElementById('directorate_code');
const submitBtn = document.getElementById('submitBtn');
const toast = document.getElementById('toast');

const filterForm = document.getElementById('filterForm');
const filterSelect = document.getElementById('filter_directorate_code');
const listContainer = document.getElementById('emailListContainer');
const emailTable = document.getElementById('emailTable');
const emailTableBody = emailTable.querySelector('tbody');
const noEmailsMessage = document.getElementById('noEmailsMessage');
const loadingMessage = document.getElementById('loadingMessage');
const errorMessage = document.getElementById('errorMessage');

// Modal Elements
const modal = document.getElementById('deleteMailingConfirmModal');
const modalTitle = document.getElementById('deleteMailingConfirmTitle');
const modalMessage = document.getElementById('deleteMailingConfirmMessage');
const confirmBtn = document.getElementById('confirmDeleteMailingBtn');
const cancelBtn = document.getElementById('cancelDeleteMailingBtn');
const modalOverlay = document.querySelector('.modal-overlay');

// State
let isLoading = false;
let emailToDelete = null;
let codeToDelete = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    saveForm.addEventListener('submit', handleSubmit);

    if (filterForm) {
        filterForm.addEventListener('submit', handleFilterSubmit);
    }

    if (cancelBtn) cancelBtn.addEventListener('click', closeModal);
    if (modalOverlay) modalOverlay.addEventListener('click', closeModal);
    if (confirmBtn) confirmBtn.addEventListener('click', handleConfirmDelete);
});

// Handle form submission
async function handleSubmit(e) {
    e.preventDefault();

    const email = emailInput.value.trim();
    const directorate_code = directorateCodeInput.value.trim();

    // Validation
    if (!email || !directorate_code) {
        showToast('Preencha todos os campos', 'error');
        return;
    }

    if (email.length > 255) {
        showToast('E-mail muito longo (máximo 255 caracteres)', 'error');
        return;
    }

    if (directorate_code.length > 50) {
        showToast('Código da diretoria muito longo (máximo 50 caracteres)', 'error');
        return;
    }

    if (isLoading) return;

    isLoading = true;
    submitBtn.disabled = true;
    submitBtn.textContent = 'Adicionando...';

    try {
        const response = await fetch(API_BASE + '/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, directorate_code }),
        });

        if (response.ok) {
            showToast('E-mail adicionado com sucesso!', 'success');

            // Update filter with the directorate used in save
            if (filterSelect) {
                filterSelect.value = directorate_code;
                // Only fetch if the value was successfully set (exists in options)
                if (filterSelect.value === directorate_code) {
                    fetchEmails(directorate_code);
                }
            }

            emailInput.value = '';
        } else {
            const error = await response.json();
            showToast(error.error || 'Erro ao adicionar e-mail', 'error');
        }
    } catch (error) {
        showToast('Erro ao adicionar e-mail', 'error');
    } finally {
        isLoading = false;
        submitBtn.disabled = false;
        submitBtn.innerHTML = `
            <svg class="icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="12" y1="5" x2="12" y2="19"/>
                <line x1="5" y1="12" x2="19" y2="12"/>
            </svg>
            Adicionar à Lista
        `;
    }
}

// Handle filter submit
function handleFilterSubmit(e) {
    e.preventDefault();
    const code = filterSelect.value;

    if (code && code !== 'null') {
        fetchEmails(code);
    } else {
        showToast('Selecione uma diretoria para filtrar', 'error');
        hideAllListElements();
    }
}

function hideAllListElements() {
    listContainer.style.display = 'none';
    emailTable.style.display = 'none';
    noEmailsMessage.style.display = 'none';
    loadingMessage.style.display = 'none';
    errorMessage.style.display = 'none';
}

// Fetch emails
async function fetchEmails(code) {

    if (!code || code === 'null') {
        return;
    }

    hideAllListElements();
    listContainer.style.display = 'block';
    loadingMessage.style.display = 'block';

    const url = `${API_BASE}/list?directorate_code=${code}`;

    try {
        const response = await fetch(url);

        if (response.ok) {
            const data = await response.json();
            renderList(data.emails, code);
        } else {
            const errorText = await response.text();
            loadingMessage.style.display = 'none';
            errorMessage.style.display = 'block';
        }
    } catch (error) {
        loadingMessage.style.display = 'none';
        errorMessage.style.display = 'block';
    }
}

// Render email list
function renderList(emails, code) {
    loadingMessage.style.display = 'none';

    if (!emails || emails.length === 0) {
        noEmailsMessage.style.display = 'block';
        return;
    }

    emailTable.style.display = 'table';
    emailTableBody.innerHTML = '';

    emails.forEach(email => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${email}</td>
            <td class="actions-cell">
                <div class="btn-action-container">
                    <button class="btn btn-danger btn-sm delete-btn" data-email="${email}" data-code="${code}" style="padding: 6px 12px; background-color: #ef4444; color: white; border: none; border-radius: 4px; cursor: pointer; display: inline-flex; align-items: center; justify-content: center;">
                        <svg class="icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="3 6 5 6 21 6"></polyline>
                            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                        </svg>
                    </button>
                </div>
            </td>
        `;
        emailTableBody.appendChild(tr);
    });

    // Add event listeners to delete buttons
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const btn = e.currentTarget;
            openDeleteModal(btn.dataset.email, btn.dataset.code);
        });
    });
}

// Open delete modal
function openDeleteModal(email, code) {
    emailToDelete = email;
    codeToDelete = code;

    let directorateLabel = code;
    if (filterSelect) {
        const option = Array.from(filterSelect.options).find(opt => opt.value === code);
        if (option) {
            directorateLabel = option.text;
        }
    }

    modalTitle.textContent = 'Confirmar exclusão';
    modalMessage.textContent = `Remover "${email}" da diretoria "${directorateLabel}"?`;
    confirmBtn.textContent = 'Remover';
    confirmBtn.disabled = false;

    modal.style.display = 'flex';
}

// Close modal
function closeModal() {
    modal.style.display = 'none';
    emailToDelete = null;
    codeToDelete = null;
}

// Handle confirm delete
async function handleConfirmDelete() {
    if (!emailToDelete || !codeToDelete) return;

    const currentCode = codeToDelete; // Capture code before closing modal
    confirmBtn.disabled = true;
    confirmBtn.textContent = 'Removendo...';

    try {
        const response = await fetch(API_BASE + '/', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email: emailToDelete, directorate_code: codeToDelete }),
        });

        if (response.ok) {
            showToast('E-mail removido com sucesso!', 'success');
            closeModal();
            setTimeout(() => {
                fetchEmails(currentCode); // Use captured code
            }, 500);
        } else {
            const error = await response.json();
            showToast(error.error || 'Erro ao remover e-mail', 'error');
            confirmBtn.disabled = false;
            confirmBtn.textContent = 'Remover';
        }
    } catch (error) {
        showToast('Erro ao remover e-mail', 'error');
        confirmBtn.disabled = false;
        confirmBtn.textContent = 'Remover';
    }
}

// Show toast notification
function showToast(message, type = 'success') {
    toast.textContent = message;
    toast.className = `toast ${type} show`;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}
