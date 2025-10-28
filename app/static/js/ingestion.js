// API Base URL
const API_BASE = '/ingestion';

// DOM Elements
const ingestForm = document.getElementById('ingestForm');
const startRowInput = document.getElementById('start_row');
const submitBtn = document.getElementById('submitBtn');
const toast = document.getElementById('toast');

// State
let isLoading = false;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    ingestForm.addEventListener('submit', handleSubmit);
});

// Handle form submission
async function handleSubmit(e) {
    e.preventDefault();

    const startRow = startRowInput.value.trim();

    // Validation
    if (!startRow || isNaN(startRow) || startRow < 1) {
        showToast('Por favor, insira uma linha de início válida.', 'error');
        return;
    }

    if (isLoading) return;

    isLoading = true;
    submitBtn.disabled = true;
    submitBtn.textContent = 'Processando...';

    try {
        const response = await fetch(API_BASE + "/ingest", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ row: parseInt(startRow, 10) }),
        });

        if (response.ok) {
            const data = await response.json();
            showToast(data.message || 'Ingestão iniciada com sucesso!', 'success');
            startRowInput.value = '';

            if (data.alerts && data.alerts.length > 0) {
                const alertId = data.alerts[0];
                try {
                    const tplResp = await fetch(`/email/render/${encodeURIComponent(alertId)}`);
                    if (tplResp.ok) {
                        const html = await tplResp.text();

                        let container = document.getElementById('emailPreviewContainer');
                        if (!container) {
                            container = document.createElement('div');
                            container.id = 'emailPreviewContainer';
                            container.style.marginTop = '20px';
                            ingestForm.parentNode.insertBefore(container, ingestForm.nextSibling);
                        }
                        container.innerHTML = html;
                    } else {
                        // servidor retornou não-OK ao tentar renderizar template
                        // não bloqueara fluxo principal; mostrar mensagem curta
                        showToast('Alerta salvo, mas falha ao gerar preview do e-mail.', 'error');
                    }
                } catch (err) {
                    showToast('Alerta salvo, mas falha ao gerar preview do e-mail.', 'error');
                }
            }
        } else {
            const contentType = response.headers.get('Content-Type');
            if (contentType && contentType.includes('application/json')) {
                const error = await response.json();
                showToast(error.error || 'Erro ao realizar a ingestão.', 'error');
            } else {
                showToast('Erro inesperado: resposta inválida do servidor.', 'error');
                console.error('Resposta inválida:', await response.text());
            }
        }
    } catch (error) {
        showToast('Erro ao realizar a ingestão.', 'error');
        console.error('Erro:', error);
    } finally {
        isLoading = false;
        submitBtn.disabled = false;
        submitBtn.textContent = 'Iniciar Ingestão';
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
