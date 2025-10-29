function showConfirmModal() {
    const emailConfirmModal = document.getElementById('emailConfirmModal');
    const sendBtnHeader = document.getElementById('sendEmailBtnHeader');
    if (emailConfirmModal) emailConfirmModal.style.display = 'flex';
    if (sendBtnHeader) sendBtnHeader.disabled = true;
}

function hideConfirmModal() {
    const emailConfirmModal = document.getElementById('emailConfirmModal');
    const recipientsList = document.getElementById('recipientsList');
    const existingCheckbox = document.getElementById('confirmSendCheckbox');
    const sendBtnHeader = document.getElementById('sendEmailBtnHeader');
    const confirmSendBtn = document.getElementById('confirmSendBtn');

    if (emailConfirmModal) emailConfirmModal.style.display = 'none';
    if (recipientsList) recipientsList.innerHTML = '';
    if (existingCheckbox) existingCheckbox.remove();
    if (sendBtnHeader) sendBtnHeader.disabled = false;
    if (confirmSendBtn) {
        confirmSendBtn.disabled = false;
        confirmSendBtn.textContent = 'Confirmar e enviar';
    }
}

function openConfirmModal(data, alertId) {
    const recipientsList = document.getElementById('recipientsList');
    const confirmSendBtn = document.getElementById('confirmSendBtn');

    if (!recipientsList) {
        console.warn('recipientsList não encontrado no DOM.');
        showConfirmModal();
        return;
    }

    const status = data && data.status ? data.status : null;
    const dests = Array.isArray(data.recipients) ? data.recipients : [];

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

        if (confirmSendBtn) {
            confirmSendBtn.disabled = true;
            confirmSendBtn.textContent = 'Confirmar e enviar';
        }
    } else {
        if (confirmSendBtn) confirmSendBtn.disabled = false;
    }

    showConfirmModal();
}

async function handleConfirmSend(alertId) {
    const confirmSendBtn = document.getElementById('confirmSendBtn');
    const sendBtnHeader = document.getElementById('sendEmailBtnHeader');

    if (!alertId) {
        showToast('Nenhum alerta selecionado para envio.', 'error');
        hideConfirmModal();
        return;
    }
    if (confirmSendBtn && confirmSendBtn.disabled) return;

    const prevText = confirmSendBtn ? confirmSendBtn.textContent : 'Confirmar e enviar';
    if (confirmSendBtn) {
        confirmSendBtn.disabled = true;
        confirmSendBtn.textContent = 'Enviando...';
    }
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
        if (confirmSendBtn) {
            confirmSendBtn.disabled = false;
            confirmSendBtn.textContent = prevText;
        }
    }
}

function cleanupAfterSend() {
    const previewContainer = document.getElementById('emailPreviewContainer');
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
    const sendBtnHeader = document.getElementById('sendEmailBtnHeader');
    if (sendBtnHeader) {
        sendBtnHeader.style.display = 'none';
        sendBtnHeader.disabled = true;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const cancelBtn = document.getElementById('cancelSendBtn');
    const confirmBtn = document.getElementById('confirmSendBtn');

    if (cancelBtn) {
        cancelBtn.addEventListener('click', (e) => {
            e.preventDefault();
            hideConfirmModal();
        });
    }

    if (confirmBtn) {
        confirmBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const previewContainer = document.getElementById('emailPreviewContainer');
            const alertId = previewContainer ? previewContainer.dataset.alertId : null;
            handleConfirmSend(alertId);
        });
    }

    document.addEventListener('change', (ev) => {
        const target = ev.target;
        if (target && target.id === 'confirmSendCheckboxInput') {
            const confirmBtn = document.getElementById('confirmSendBtn');
            if (confirmBtn) confirmBtn.disabled = !target.checked;
        }
    });
});
