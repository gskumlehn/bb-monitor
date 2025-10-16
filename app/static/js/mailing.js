// API Base URL
const API_BASE = '/mailing';

// DOM Elements
const addForm = document.getElementById('addForm');
const emailInput = document.getElementById('email');
const directorateCodeInput = document.getElementById('directorate_code');
const submitBtn = document.getElementById('submitBtn');
const toast = document.getElementById('toast');

// State
let isLoading = false;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    addForm.addEventListener('submit', handleSubmit);
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
        const response = await fetch(API_BASE, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, directorate_code }),
        });

        if (response.ok) {
            showToast('E-mail adicionado com sucesso!', 'success');
            emailInput.value = '';
            directorateCodeInput.value = '';
        } else {
            const error = await response.json();
            showToast(error.error || 'Erro ao adicionar e-mail', 'error');
        }
    } catch (error) {
        showToast('Erro ao adicionar e-mail', 'error');
        console.error('Erro:', error);
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

// Show toast notification
function showToast(message, type = 'success') {
    toast.textContent = message;
    toast.className = `toast ${type} show`;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}
