// API Base URL
const API_BASE = '/ingestion';

// DOM Elements
const ingestForm = document.getElementById('ingestForm');
const startRowInput = document.getElementById('start_row');
const submitBtn = document.getElementById('submitBtn');
const toast = document.getElementById('toast');
const previewContainer = document.getElementById('emailPreviewContainer');
const sendBtn = document.getElementById('sendEmailBtn');

// State
let isLoading = false;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    ingestForm.addEventListener('submit', handleSubmit);

    if (sendBtn) {
        sendBtn.addEventListener('click', async () => {
            const alertId = previewContainer ? previewContainer.dataset.alertId : null;
            if (!alertId) {
                showToast('Nenhum alerta selecionado para envio.', 'error');
                return;
            }
            if (sendBtn.disabled) return;
            sendBtn.disabled = true;
            const prevText = sendBtn.textContent;
            sendBtn.textContent = 'Enviando...';
            try {
                const resp = await fetch(`/email/send/${encodeURIComponent(alertId)}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({})
                });
                if (resp.ok) {
                    const resJson = await resp.json();
                    showToast(resJson.message || 'Email enviado com sucesso', 'success');
                } else {
                    const ct = resp.headers.get('Content-Type') || '';
                    if (ct.includes('application/json')) {
                        const err = await resp.json();
                        showToast(err.description || err.error || 'Falha ao enviar email', 'error');
                    } else {
                        const txt = await resp.text();
                        showToast('Falha ao enviar email', 'error');
                        console.error('Erro envio email:', txt);
                    }
                }
            } catch (err) {
                showToast('Erro ao enviar email.', 'error');
                console.error(err);
            } finally {
                sendBtn.disabled = false;
                sendBtn.textContent = prevText;
            }
        });
    }
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

            if (data.alerts && data.alerts.length > 0) {
                const alertId = data.alerts[0];
                try {
                    const tplResp = await fetch(`/email/render/${encodeURIComponent(alertId)}`);
                    if (tplResp.ok) {
                        const html = await tplResp.text();

                        const headerHtml = `<div style="margin-bottom:8px;font-size:14px;color:#333;">Preview de email gerado pela linha: <strong>${startRow}</strong></div>`;

                        if (!previewContainer) {
                            showToast('Preview container não encontrado.', 'error');
                            return;
                        }

                        previewContainer.dataset.startRow = startRow;
                        previewContainer.dataset.alertId = alertId;
                        previewContainer.innerHTML = headerHtml + html;

                        if (sendBtn) {
                            sendBtn.style.display = ''; // mostrar
                            sendBtn.disabled = false;
                            sendBtn.textContent = 'Enviar email';
                        }
                    } else {
                        showToast('Alerta salvo, mas falha ao gerar preview do e-mail.', 'error');
                        if (sendBtn) {
                            sendBtn.style.display = 'none';
                        }
                    }
                } catch (err) {
                    showToast('Alerta salvo, mas falha ao gerar preview do e-mail.', 'error');
                    if (sendBtn) {
                        sendBtn.style.display = 'none';
                    }
                }
            } else {
                if (sendBtn) sendBtn.style.display = 'none';
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
