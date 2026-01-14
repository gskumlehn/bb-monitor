const API_BASE = '/ingestion';

const ingestForm = document.getElementById('ingestForm');
const startRowInput = document.getElementById('start_row');
const submitBtn = document.getElementById('submitBtn');
const toast = document.getElementById('toast');

const previewCard = document.getElementById('emailPreviewCard');
const previewContainer = document.getElementById('emailPreviewContainer');
const sendBtnHeader = document.getElementById('sendEmailBtnHeader');
const previewTitle = document.getElementById('previewTitle');

let isLoading = false;

document.addEventListener('DOMContentLoaded', () => {
    ingestForm.addEventListener('submit', handleSubmit);

    if (sendBtnHeader) {
        sendBtnHeader.addEventListener('click', handleSendClick);
    }
});

async function handleSendClick() {
    const alertId = previewCard ? previewCard.dataset.alertId : null;
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
        const status = data && data.status !== undefined && data.status !== null
            ? String(data.status).toUpperCase().trim()
            : null;

        const toList = Array.isArray(data.recipients) ? data.recipients : [];
        const ccList = Array.isArray(data.cc) ? data.cc : [];

        if (typeof openConfirmModal === 'function') {
            openConfirmModal({ status, recipients: toList, cc: ccList }, alertId);
        }
    } catch (err) {
        if (sendBtnHeader) {
            sendBtnHeader.disabled = false;
            sendBtnHeader.textContent = 'Enviar email';
        }
        showToast('Erro ao consultar dados de validação.', 'error');
    }
}

async function handleSubmit(e) {
    e.preventDefault();

    const startRow = startRowInput.value.trim();

    // Reset preview area
    if (previewCard) {
        previewCard.style.display = 'none';
        delete previewCard.dataset.alertId;
    }
    if (previewContainer) {
        previewContainer.innerHTML = '';
    }
    if (sendBtnHeader) {
        sendBtnHeader.disabled = true;
    }
    if (previewTitle) {
        previewTitle.textContent = 'Preview do Email';
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
                const alertId = String(data.alerts[0]);

                if (!alertId) {
                    showToast('ID do alerta inválido retornado pelo servidor.', 'error');
                    return;
                }

                try {
                    const tplResp = await fetch(`/email/render/${encodeURIComponent(alertId)}`);
                    if (tplResp.ok) {
                        const html = await tplResp.text();

                        if (previewCard && previewContainer) {
                            previewContainer.innerHTML = html;
                            previewCard.dataset.alertId = alertId;

                            if (previewTitle) {
                                previewTitle.textContent = 'Preview do Email';
                            }

                            const btnInPreview = previewContainer.querySelector('#sendEmailBtn');
                            if (btnInPreview) btnInPreview.remove();

                            previewCard.style.display = 'block';

                            if (sendBtnHeader) {
                                sendBtnHeader.disabled = false;
                            }
                        }
                    } else {
                        showToast('Alerta salvo, mas falha ao gerar preview do e-mail.', 'error');
                    }
                } catch (err) {
                    showToast('Alerta salvo, mas falha ao gerar preview do e-mail.', 'error');
                }
            } else {
                showToast('Nenhum alerta foi gerado ou retornado.', 'warning');
            }
        } else {
            const contentType = response.headers.get('Content-Type');
            if (contentType && contentType.includes('application/json')) {
                const error = await response.json();
                showToast(error.error || 'Erro ao realizar a ingestão.', 'error');
            } else {
                showToast('Erro inesperado: resposta inválida do servidor.', 'error');
            }
        }
    } catch (error) {
        showToast('Erro ao realizar a ingestão.', 'error');
    } finally {
        isLoading = false;
        submitBtn.disabled = false;
        submitBtn.textContent = 'Gerar email';
    }
}

function showToast(message, type = 'success') {
    toast.textContent = message;
    toast.className = `toast ${type} show`;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}
