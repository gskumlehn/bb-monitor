const API_BASE = '/ingestion';

const ingestForm = document.getElementById('ingestForm');
const startRowInput = document.getElementById('start_row');
const submitBtn = document.getElementById('submitBtn');
const toast = document.getElementById('toast');
const previewContainer = document.getElementById('emailPreviewContainer');
const sendBtnHeader = document.getElementById('sendEmailBtnHeader');

let isLoading = false;

document.addEventListener('DOMContentLoaded', () => {
    ingestForm.addEventListener('submit', handleSubmit);

    if (sendBtnHeader) {
        sendBtnHeader.addEventListener('click', handleSendClick);
    }
});

async function handleSendClick() {
    const alertId = previewContainer ? previewContainer.dataset.alertId : null;
    if (!alertId) {
        showToast('Nenhum alerta selecionado para envio.', 'error');
        return;
    }
    try {
        sendBtnHeader.disabled = true;
        sendBtnHeader.textContent = 'Carregando...';
        const resp = await fetch(`/email/validate/${encodeURIComponent(alertId)}`);
        sendBtnHeader.textContent = 'Enviar email';
        if (!resp.ok) {
            sendBtnHeader.disabled = false;
            showToast('Falha ao obter dados de validação para confirmação.', 'error');
            return;
        }
        const data = await resp.json();
        const status = data && data.status ? data.status : null;
        const dests = Array.isArray(data.recipients) ? data.recipients : [];

        if (typeof openConfirmModal === 'function') {
            openConfirmModal({ status, recipients: dests }, alertId);
        } else {
            console.warn('openConfirmModal não encontrado: verifique se email_confirm.js foi carregado.');
        }
    } catch (err) {
        if (sendBtnHeader) {
            sendBtnHeader.disabled = false;
            sendBtnHeader.textContent = 'Enviar email';
        }
        showToast('Erro ao consultar dados de validação.', 'error');
        console.error(err);
    }
}

async function handleSubmit(e) {
    e.preventDefault();

    const startRow = startRowInput.value.trim();

    if (previewContainer) {
        previewContainer.innerHTML = '';
        delete previewContainer.dataset.startRow;
        delete previewContainer.dataset.alertId;
    }
    const previewHeader = document.getElementById('emailPreviewHeader');
    const previewStartRowEl = document.getElementById('previewStartRow');
    const previewAlertIdEl = document.getElementById('previewAlertId');
    if (previewHeader) {
        previewHeader.style.display = 'none';
    }
    if (previewStartRowEl) previewStartRowEl.textContent = '';
    if (previewAlertIdEl) previewAlertIdEl.textContent = '';
    if (sendBtnHeader) {
        sendBtnHeader.style.display = 'none';
        sendBtnHeader.disabled = true;
    }

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

                        if (!previewContainer) {
                            showToast('Preview container não encontrado.', 'error');
                            return;
                        }

                        if (previewHeader && previewStartRowEl && previewAlertIdEl) {
                            previewStartRowEl.textContent = startRow;
                            previewAlertIdEl.textContent = alertId;
                            previewHeader.style.display = '';
                        }

                        previewContainer.dataset.startRow = startRow;
                        previewContainer.dataset.alertId = alertId;
                        previewContainer.innerHTML = html;

                        const btnInPreview = previewContainer.querySelector('#sendEmailBtn');
                        if (btnInPreview) btnInPreview.remove();

                        if (sendBtnHeader) {
                            sendBtnHeader.style.display = '';
                            sendBtnHeader.disabled = false;
                            sendBtnHeader.textContent = 'Enviar email';
                        }
                    } else {
                        showToast('Alerta salvo, mas falha ao gerar preview do e-mail.', 'error');
                        if (sendBtnHeader) {
                            sendBtnHeader.style.display = 'none';
                            sendBtnHeader.disabled = true;
                        }
                        if (previewHeader) previewHeader.style.display = 'none';
                    }
                } catch (err) {
                    showToast('Alerta salvo, mas falha ao gerar preview do e-mail.', 'error');
                    if (sendBtnHeader) {
                        sendBtnHeader.style.display = 'none';
                        sendBtnHeader.disabled = true;
                    }
                    if (previewHeader) previewHeader.style.display = 'none';
                }
            } else {
                if (sendBtnHeader) {
                    sendBtnHeader.style.display = 'none';
                    sendBtnHeader.disabled = true;
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
        const previewHeader = document.getElementById('emailPreviewHeader');
        if (previewHeader) previewHeader.style.display = 'none';
        if (sendBtnHeader) {
            sendBtnHeader.style.display = 'none';
            sendBtnHeader.disabled = true;
        }
    } finally {
        isLoading = false;
        submitBtn.disabled = false;
        submitBtn.textContent = 'Iniciar Ingestão';
    }
}

function showToast(message, type = 'success') {
    toast.textContent = message;
    toast.className = `toast ${type} show`;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}
