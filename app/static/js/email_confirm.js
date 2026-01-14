function showConfirmModal() {
    const emailConfirmModal = document.getElementById('emailConfirmModal');
    const sendBtnHeader = document.getElementById('sendEmailBtnHeader');
    if (emailConfirmModal) emailConfirmModal.style.display = 'flex';
    if (sendBtnHeader) sendBtnHeader.disabled = true;
}

function hideConfirmModal() {
    const emailConfirmModal = document.getElementById('emailConfirmModal');
    const recipientsList = document.getElementById('recipientsList');
    const ccList = document.getElementById('ccList');
    const wrapper = document.getElementById('confirmSendCheckbox');
    const checkboxInput = document.getElementById('confirmSendCheckboxInput');
    const sendBtnHeader = document.getElementById('sendEmailBtnHeader');
    const confirmSendBtn = document.getElementById('confirmSendBtn');

    if (emailConfirmModal) {
        emailConfirmModal.style.display = 'none';
        delete emailConfirmModal.dataset.alertId;
    }
    if (recipientsList) recipientsList.innerHTML = '';
    if (ccList) ccList.innerHTML = '';
    if (wrapper) wrapper.style.display = 'none';
    if (checkboxInput) {
        checkboxInput.checked = false;
    }
    if (sendBtnHeader) sendBtnHeader.disabled = false;
    if (confirmSendBtn) {
        confirmSendBtn.disabled = false;
        confirmSendBtn.textContent = 'Confirmar e enviar';
    }
}

function openConfirmModal(data, alertId) {
    const recipientsList = document.getElementById('recipientsList');
    const ccList = document.getElementById('ccList');
    const recipientsContainer = document.getElementById('recipientsListContainer');
    const ccContainer = document.getElementById('ccListContainer');
    const confirmSendBtn = document.getElementById('confirmSendBtn');
    const emailConfirmModal = document.getElementById('emailConfirmModal');
    const wrapper = document.getElementById('confirmSendCheckbox');
    const checkboxInput = document.getElementById('confirmSendCheckboxInput');
    const messageSpan = document.getElementById('confirmSendCheckboxMessage');

    if (!recipientsList || !recipientsContainer || !emailConfirmModal || !wrapper || !checkboxInput || !messageSpan) {
        console.warn('Elemento de modal/recipients/checkbox não encontrado no DOM.');
        showConfirmModal();
        return;
    }

    if (alertId) {
        emailConfirmModal.dataset.alertId = alertId;
    }

    const rawStatus = data && data.status ? data.status : null;
    const status = rawStatus !== null && rawStatus !== undefined ? String(rawStatus).toUpperCase().trim() : null;

    // support both "recipients" (primary) and "cc" arrays
    const toList = Array.isArray(data.recipients) ? data.recipients : [];
    const ccListArr = Array.isArray(data.cc) ? data.cc : [];

    if (toList.length === 0) {
        recipientsList.innerHTML = '<li style="color:var(--muted-foreground);">Nenhum destinatário encontrado.</li>';
    } else {
        recipientsList.innerHTML = toList.map(d => `<li style="padding:6px 0; border-bottom:1px solid rgba(0,0,0,0.04);">${d}</li>`).join('');
    }

    if (ccListArr.length === 0) {
        ccList.innerHTML = '<li style="color:var(--muted-foreground);">Nenhum e-mail em cópia.</li>';
    } else {
        ccList.innerHTML = ccListArr.map(d => `<li style="padding:6px 0; border-bottom:1px solid rgba(0,0,0,0.04);">${d}</li>`).join('');
    }

    checkboxInput.checked = false;
    wrapper.style.display = 'none';

    const needsConfirmation = (status === 'NOT_SENT' || status === 'EMAIL_SENT');

    if (needsConfirmation) {
        const msgMap = {
            'NOT_SENT': 'O alerta não foi enviado por Whatsapp, enviar por email?',
            'EMAIL_SENT': 'O alerta já foi enviado por email, enviar novamente?'
        };
        const message = msgMap[status] || 'Deseja realmente enviar este alerta por email?';
        messageSpan.textContent = message;

        wrapper.style.display = 'block';
        if (confirmSendBtn) {
            confirmSendBtn.disabled = true;
            confirmSendBtn.textContent = 'Confirmar e enviar';
        }
    } else {
        wrapper.style.display = 'none';
        if (confirmSendBtn) confirmSendBtn.disabled = false;
    }

    showConfirmModal();
}

async function handleConfirmSend(passedAlertId) {
    const confirmSendBtn = document.getElementById('confirmSendBtn');
    const sendBtnHeader = document.getElementById('sendEmailBtnHeader');
    const emailConfirmModal = document.getElementById('emailConfirmModal');

    const alertId = passedAlertId || (emailConfirmModal && emailConfirmModal.dataset ? emailConfirmModal.dataset.alertId : null);
    if (!alertId) {
        showToast('Nenhum alerta selecionado para envio.', 'error');
        hideConfirmModal();
        return;
    }

    const checkboxInput = document.getElementById('confirmSendCheckboxInput');
    const wrapper = document.getElementById('confirmSendCheckbox');
    if (wrapper && wrapper.style.display !== 'none' && checkboxInput && !checkboxInput.checked) {
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
    const previewCard = document.getElementById('emailPreviewCard');
    const previewContainer = document.getElementById('emailPreviewContainer');

    if (previewContainer) {
        previewContainer.innerHTML = '';
    }

    if (previewCard) {
        previewCard.style.display = 'none';
        delete previewCard.dataset.alertId;
    }

    const sendBtnHeader = document.getElementById('sendEmailBtnHeader');
    if (sendBtnHeader) {
        sendBtnHeader.disabled = true;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const cancelBtn = document.getElementById('cancelSendBtn');
    const confirmBtn = document.getElementById('confirmSendBtn');
    const checkboxInput = document.getElementById('confirmSendCheckboxInput');

    if (cancelBtn) {
        cancelBtn.addEventListener('click', (e) => {
            e.preventDefault();
            hideConfirmModal();
        });
    }

    if (confirmBtn) {
        confirmBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const previewCard = document.getElementById('emailPreviewCard');
            const alertId = previewCard ? previewCard.dataset.alertId : null;
            handleConfirmSend(alertId);
        });
    }

    if (checkboxInput) {
        checkboxInput.addEventListener('change', function () {
            const confirmBtnLocal = document.getElementById('confirmSendBtn');
            if (confirmBtnLocal) confirmBtnLocal.disabled = !this.checked;
        });
    }
});
