document.addEventListener('DOMContentLoaded', function () {
    const validateSentMailingUrl = document.getElementById('assignForm').dataset.validateUrl;
    const sendMailingUrl = document.getElementById('assignForm').dataset.sendUrl;

    const form = document.getElementById('assignForm');
    const submitBtn = document.getElementById('submitBtn');
    const mailingConfirmModal = document.getElementById('mailingConfirmModal');
    const alertedDirectoratesList = document.getElementById('alertedDirectoratesList');
    const confirmSendCheckboxInput = document.getElementById('confirmSendCheckboxInput');
    const confirmSendBtn = document.getElementById('confirmSendBtn');
    const cancelSendBtn = document.getElementById('cancelSendBtn');
    const toast = document.getElementById('toast');

    function setLoading(isLoading) {
        if (!submitBtn) return;
        if (isLoading) {
            submitBtn.classList.add('loading');
            submitBtn.disabled = true;
        } else {
            submitBtn.classList.remove('loading');
            submitBtn.disabled = false;
        }
    }

    function showToast(message, type = 'success') {
        if (!toast) return;
        toast.textContent = message;
        toast.className = `toast ${type} show`;

        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }

    async function validateSentMailing() {
        try {
            const response = await fetch(validateSentMailingUrl, { method: 'POST' });
            if (response.ok) {
                const data = await response.json();
                return data.alerted_directorates || [];
            } else {
                console.error('Erro ao validar envio anterior:', await response.text());
                return [];
            }
        } catch (err) {
            console.error('Erro ao validar envio anterior:', err);
            return [];
        }
    }

    async function sendMailing(selectedDirectorates) {
        try {
            const response = await fetch(sendMailingUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ directorates: selectedDirectorates }),
            });
            if (response.ok) {
                const data = await response.json();
                showToast('Mailing enviado com sucesso!', 'success');
            } else {
                const errorText = await response.text();
                showToast(`Erro ao enviar mailing: ${errorText}`, 'error');
            }
        } catch (err) {
            console.error('Erro ao enviar mailing:', err);
            showToast('Erro ao enviar mailing. Tente novamente mais tarde.', 'error');
        } finally {
            setLoading(false);
        }
    }

    function openMailingConfirmModal(alertedDirectorates, selectedDirectorates) {
        if (!mailingConfirmModal || !alertedDirectoratesList) return;

        // Preencher a lista de diretorias alertadas
        alertedDirectoratesList.innerHTML = '';
        alertedDirectorates.forEach(directorate => {
            const li = document.createElement('li');
            li.textContent = directorate;
            alertedDirectoratesList.appendChild(li);
        });

        // Exibir a modal
        mailingConfirmModal.style.display = 'flex';

        // Gerenciar o botão de confirmação
        confirmSendCheckboxInput.checked = false;
        confirmSendBtn.disabled = true;

        confirmSendCheckboxInput.addEventListener('change', function () {
            confirmSendBtn.disabled = !this.checked;
        });

        confirmSendBtn.addEventListener('click', function () {
            mailingConfirmModal.style.display = 'none';
            sendMailing(selectedDirectorates);
        });

        cancelSendBtn.addEventListener('click', function () {
            mailingConfirmModal.style.display = 'none';
            setLoading(false); // Parar o loading se o envio for cancelado
        });
    }

    if (form) {
        form.addEventListener('submit', async function (e) {
            e.preventDefault();

            const selectedDirectorates = Array.from(document.querySelectorAll('.checkbox-input'))
                .filter(i => i.checked)
                .map(i => i.name);

            if (selectedDirectorates.length === 0) {
                showToast('Selecione pelo menos uma diretoria para enviar o mailing.', 'error');
                return;
            }

            setLoading(true);
            const alertedDirectorates = await validateSentMailing();

            if (alertedDirectorates.length > 0) {
                openMailingConfirmModal(alertedDirectorates, selectedDirectorates);
            } else {
                await sendMailing(selectedDirectorates);
            }
        });
    }
});
