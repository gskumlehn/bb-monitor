const API_BASE = '/mailing';

const saveForm = document.getElementById('saveForm');
const emailInput = document.getElementById('email');
const directorateCodeInput = document.getElementById('directorate_code');
const submitBtn = document.getElementById('submitBtn');
const toast = document.getElementById('toast');

const filterForm = document.getElementById('filterForm');
const filterSelect = document.getElementById('filter_directorate_code');
const filterEmailInput = document.getElementById('filter_email');
const filterByDirectorateGroup = document.getElementById('filterByDirectorateGroup');
const filterByEmailGroup = document.getElementById('filterByEmailGroup');

const listContainer = document.getElementById('listContainer');
const resultsTable = document.getElementById('resultsTable');
const resultsTableBody = resultsTable.querySelector('tbody');
const resultHeaderMain = document.getElementById('resultHeaderMain');
const noResultsMessage = document.getElementById('noResultsMessage');
const loadingMessage = document.getElementById('loadingMessage');
const errorMessage = document.getElementById('errorMessage');

const tabListEmails = document.getElementById('tabListEmails');
const tabListDirectorates = document.getElementById('tabListDirectorates');

const modal = document.getElementById('deleteMailingConfirmModal');
const modalTitle = document.getElementById('deleteMailingConfirmTitle');
const modalMessage = document.getElementById('deleteMailingConfirmMessage');
const confirmBtn = document.getElementById('confirmDeleteMailingBtn');
const cancelBtn = document.getElementById('cancelDeleteMailingBtn');
const modalOverlay = document.querySelector('.modal-overlay');

let isLoading = false;
let emailToDelete = null;
let codeToDelete = null;
let currentMode = 'emails';

document.addEventListener('DOMContentLoaded', () => {
    saveForm.addEventListener('submit', handleSubmit);

    if (filterForm) {
        filterForm.addEventListener('submit', handleFilterSubmit);
    }

    if (tabListEmails) {
        tabListEmails.addEventListener('click', () => switchMode('emails'));
    }
    if (tabListDirectorates) {
        tabListDirectorates.addEventListener('click', () => switchMode('directorates'));
    }

    if (cancelBtn) cancelBtn.addEventListener('click', closeModal);
    if (modalOverlay) modalOverlay.addEventListener('click', closeModal);
    if (confirmBtn) confirmBtn.addEventListener('click', handleConfirmDelete);
});

function switchMode(mode) {
    if (currentMode === mode) return;
    currentMode = mode;

    if (mode === 'emails') {
        tabListEmails.classList.add('active');
        tabListDirectorates.classList.remove('active');
        filterByDirectorateGroup.style.display = 'block';
        filterByEmailGroup.style.display = 'none';
        resultHeaderMain.textContent = 'E-mail';
    } else {
        tabListEmails.classList.remove('active');
        tabListDirectorates.classList.add('active');
        filterByDirectorateGroup.style.display = 'none';
        filterByEmailGroup.style.display = 'block';
        resultHeaderMain.textContent = 'Diretoria';
    }

    hideAllListElements();
    resultsTableBody.innerHTML = '';
}

async function handleSubmit(e) {
    e.preventDefault();

    const email = emailInput.value.trim();
    const directorate_code = directorateCodeInput.value.trim();

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

            if (currentMode === 'emails' && filterSelect) {
                filterSelect.value = directorate_code;
                if (filterSelect.value === directorate_code) {
                    fetchEmails(directorate_code);
                }
            } else if (currentMode === 'directorates' && filterEmailInput) {
                filterEmailInput.value = email;
                fetchDirectorates(email);
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

function handleFilterSubmit(e) {
    e.preventDefault();

    if (currentMode === 'emails') {
        const code = filterSelect.value;
        if (code && code !== 'null') {
            fetchEmails(code);
        } else {
            showToast('Selecione uma diretoria para filtrar', 'error');
            hideAllListElements();
        }
    } else {
        const email = filterEmailInput.value.trim();
        if (email) {
            fetchDirectorates(email);
        } else {
            showToast('Digite um e-mail para filtrar', 'error');
            hideAllListElements();
        }
    }
}

function hideAllListElements() {
    listContainer.style.display = 'none';
    resultsTable.style.display = 'none';
    noResultsMessage.style.display = 'none';
    loadingMessage.style.display = 'none';
    errorMessage.style.display = 'none';
}

async function fetchEmails(code) {
    if (!code || code === 'null') return;

    hideAllListElements();
    listContainer.style.display = 'block';
    loadingMessage.style.display = 'block';

    const url = `${API_BASE}/list?directorate_code=${code}`;

    try {
        const response = await fetch(url);

        if (response.ok) {
            const data = await response.json();
            renderList(data.emails, code, 'email');
        } else {
            loadingMessage.style.display = 'none';
            errorMessage.style.display = 'block';
        }
    } catch (error) {
        loadingMessage.style.display = 'none';
        errorMessage.style.display = 'block';
    }
}

async function fetchDirectorates(email) {
    if (!email) return;

    hideAllListElements();
    listContainer.style.display = 'block';
    loadingMessage.style.display = 'block';

    const url = `${API_BASE}/list_directorates?email=${encodeURIComponent(email)}`;

    try {
        const response = await fetch(url);

        if (response.ok) {
            const data = await response.json();
            renderList(data.directorates, email, 'directorate');
        } else {
            const error = await response.json();
            showToast(error.error || 'Erro ao buscar diretorias', 'error');
            loadingMessage.style.display = 'none';
            if (!error.error) errorMessage.style.display = 'block';
        }
    } catch (error) {
        loadingMessage.style.display = 'none';
        errorMessage.style.display = 'block';
    }
}

function renderList(items, filterValue, type) {
    loadingMessage.style.display = 'none';

    if (!items || items.length === 0) {
        noResultsMessage.style.display = 'block';
        noResultsMessage.textContent = type === 'email'
            ? 'Nenhum e-mail encontrado para esta diretoria.'
            : 'Nenhuma diretoria encontrada para este e-mail.';
        return;
    }

    resultsTable.style.display = 'table';
    resultsTableBody.innerHTML = '';

    items.forEach(item => {
        const tr = document.createElement('tr');

        let email, code, displayValue;
        if (type === 'email') {
            email = item;
            code = filterValue;
            displayValue = email;
        } else {
            email = filterValue;
            code = item;
            displayValue = (typeof DIRECTORATE_LABELS !== 'undefined' && DIRECTORATE_LABELS[code])
                ? DIRECTORATE_LABELS[code]
                : code;
        }

        tr.innerHTML = `
            <td>${displayValue}</td>
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
        resultsTableBody.appendChild(tr);
    });

    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const btn = e.currentTarget;
            openDeleteModal(btn.dataset.email, btn.dataset.code);
        });
    });
}

function openDeleteModal(email, code) {
    emailToDelete = email;
    codeToDelete = code;

    let directorateLabel = code;
    if (typeof DIRECTORATE_LABELS !== 'undefined' && DIRECTORATE_LABELS[code]) {
        directorateLabel = DIRECTORATE_LABELS[code];
    }

    modalTitle.textContent = 'Confirmar exclusão';
    modalMessage.textContent = `Remover associação entre "${email}" e "${directorateLabel}"?`;
    confirmBtn.textContent = 'Remover';
    confirmBtn.disabled = false;

    modal.style.display = 'flex';
}

function closeModal() {
    modal.style.display = 'none';
    emailToDelete = null;
    codeToDelete = null;
}

async function handleConfirmDelete() {
    if (!emailToDelete || !codeToDelete) return;

    const savedMode = currentMode;
    const savedFilterValue = savedMode === 'emails' ? codeToDelete : emailToDelete;

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
            showToast('Removido com sucesso!', 'success');
            closeModal();

            setTimeout(() => {
                if (savedMode === 'emails') {
                    fetchEmails(savedFilterValue);
                } else {
                    fetchDirectorates(savedFilterValue);
                }
            }, 500);
        } else {
            const error = await response.json();
            showToast(error.error || 'Erro ao remover', 'error');
            confirmBtn.disabled = false;
            confirmBtn.textContent = 'Remover';
        }
    } catch (error) {
        showToast('Erro ao remover', 'error');
        confirmBtn.disabled = false;
        confirmBtn.textContent = 'Remover';
    }
}

function showToast(message, type = 'success') {
    toast.textContent = message;
    toast.className = `toast ${type} show`;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}
