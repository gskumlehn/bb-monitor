const API_BASE = '/ingestion';

const ingestForm = document.getElementById('ingestForm');
const startRowInput = document.getElementById('start_row');
const submitBtn = document.getElementById('submitBtn');
const toast = document.getElementById('toast');
const previewContainer = document.getElementById('emailPreviewContainer');
const sendBtnHeader = document.getElementById('sendEmailBtnHeader');

const emailConfirmModal = document.getElementById('emailConfirmModal');
const recipientsList = document.getElementById('recipientsList');
const confirmSendBtn = document.getElementById('confirmSendBtn');
const cancelSendBtn = document.getElementById('cancelSendBtn');

let isLoading = false;

document.addEventListener('DOMContentLoaded', () => {
    ingestForm.addEventListener('submit', handleSubmit);

    if (sendBtnHeader) {
        sendBtnHeader.addEventListener('click', handleSendClick);
    }
    if (confirmSendBtn) {
        confirmSendBtn.addEventListener('click', handleConfirmSend);
    }
    if (cancelSendBtn) {
        cancelSendBtn.addEventListener('click', hideConfirmModal);
    }
});

function showConfirmModal() {
    if (emailConfirmModal) emailConfirmModal.style.display = 'flex';
    if (sendBtnHeader) {
        sendBtnHeader.disabled = true;
    }
}

function hideConfirmModal() {
    if (emailConfirmModal) emailConfirmModal.style.display = 'none';
    if (recipientsList) recipientsList.innerHTML = '';
    const existingCheckbox = document.getElementById('confirmSendCheckbox');
    if (existingCheckbox) existingCheckbox.remove();
    if (sendBtnHeader) {
        sendBtnHeader.disabled = false;
    }
    if (confirmSendBtn) {
        confirmSendBtn.disabled = false;
        confirmSendBtn.textContent = 'Confirmar e enviar';
    }
}

function cleanupAfterSend() {
    const previewHeader = document.getElementById('emailPreviewHeader');
    if (previewContainer) {
        previewContainer.innerHTML = '';
        delete previewContainer.dataset.startRow;
        delete previewContainer.dataset.alertId;
    }
    if (previewHeader) {
        previewHeader.style.display = 'none';
        const previewStartRowEl = document.getElementById('previewStartRow');
        const previewAlertIdEl = document.getElementById('previewAlertId');
        if (previewStartRowEl) previewStartRowEl.textContent = '';
        if (previewAlertIdEl) previewAlertIdEl.textContent = '';
    }
    if (sendBtnHeader) {
        sendBtnHeader.style.display = 'none';
        sendBtnHeader.disabled = true;
    }
}

async function handleSendClick() {
    const alertId = previewContainer ? previewContainer.dataset.alertId : null;
    if (!alertId) {
        showToast('Nenhum alerta selecionado para envio.', 'error');
        return;
    }
    try {
        sendBtnHeader.disabled = true;
        sendBtnHeader.textContent = 'Carregando...';
        const resp = await fetch(`/email/recipients/${encodeURIComponent(alertId)}`);
        sendBtnHeader.textContent = 'Enviar email';
        if (!resp.ok) {
            sendBtnHeader.disabled = false;
            showToast('Falha ao obter destinatários para confirmação.', 'error');
            return;
        }
        const data = await resp.json();
        const status = data && data.status ? data.status : null;
        const dests = Array.isArray(data.recipients) ? data.recipients : [];
        if (recipientsList) {
            let statusHtml = '';
            if (dests.length === 0) {
                recipientsList.innerHTML = statusHtml + '<li style="color:var(--muted-foreground);">Nenhum destinatário encontrado.</li>';
            } else {
                recipientsList.innerHTML = statusHtml + dests.map(d => `<li style="padding:6px 0; border-bottom:1px solid rgba(0,0,0,0.04);">${d}</li>`).join('');
            }
            const existingCheckbox = document.getElementById('confirmSendCheckbox');
            if (existingCheckbox) existingCheckbox.remove();

            if (status !== 'SENT') {
                const msgMap = {
                    'NOT_SENT': 'O alerta não foi enviado por Whatsapp, realmente deve enviar por email?',
                    'EMAIL_SENT': 'O alerta já foi enviado por email, realmente deve enviar novamente?'
                };
                const message = msgMap[status] || 'Deseja realmente enviar este alerta por email?';
                const checkboxHtml = `<div id="confirmSendCheckbox" style="margin:8px 0;"><label style="display:flex;align-items:center;gap:8px;"><input type="checkbox" id="confirmSendCheckboxInput"> <span>${message}</span></label></div>`;
                recipientsList.insertAdjacentHTML('beforebegin', checkboxHtml);
                const checkboxInput = document.getElementById('confirmSendCheckboxInput');
                if (confirmSendBtn) {
                    confirmSendBtn.disabled = true;
                    confirmSendBtn.textContent = 'Confirmar e enviar';
                }
                if (checkboxInput) {
                    checkboxInput.addEventListener('change', function () {
                        if (confirmSendBtn) confirmSendBtn.disabled = !this.checked;
                    });
                }
            } else {
                if (confirmSendBtn) confirmSendBtn.disabled = false;
            }
        }
        showConfirmModal();
    } catch (err) {
        if (sendBtnHeader) {
            sendBtnHeader.disabled = false;
            sendBtnHeader.textContent = 'Enviar email';
        }
        showToast('Erro ao consultar destinatários.', 'error');
        console.error(err);
    }
}

async function handleConfirmSend() {
    const alertId = previewContainer ? previewContainer.dataset.alertId : null;
    if (!alertId) {
        showToast('Nenhum alerta selecionado para envio.', 'error');
        hideConfirmModal();
        return;
    }
    if (confirmSendBtn.disabled) return;

    const prevText = confirmSendBtn.textContent;
    confirmSendBtn.disabled = true;
    confirmSendBtn.textContent = 'Enviando...';
    if (sendBtnHeader) {
        sendBtnHeader.disabled = true;
        sendBtnHeader.textContent = 'Enviando...';
    }

    try {
        const resp = await fetch(`/email/send/${encodeURIComponent(alertId)}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({})
        });
        if (resp.ok) {
            const resJson = await resp.json();
            showToast(resJson.message || 'Email enviado com sucesso', 'success');
            hideConfirmModal();
            cleanupAfterSend();
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
            if (sendBtnHeader) {
                sendBtnHeader.disabled = false;
                sendBtnHeader.textContent = 'Enviar email';
            }
        }
    } catch (err) {
        showToast('Erro ao enviar email.', 'error');
        console.error(err);
        if (sendBtnHeader) {
            sendBtnHeader.disabled = false;
            sendBtnHeader.textContent = 'Enviar email';
        }
    } finally {
        confirmSendBtn.disabled = false;
        confirmSendBtn.textContent = prevText;
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
