function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    if (!toast) {
        return;
    }

    toast.textContent = message;
    toast.className = `toast ${type} show`;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

const ASSIGN_API = {
    VALIDATE_SENT_MAILING: document.getElementById('assignForm')?.dataset.validateUrl,
    SEND_MAILING: document.getElementById('assignForm')?.dataset.sendUrl,
};

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('assignForm');
    const submitBtn = document.getElementById('submitBtn');

    if (!form) {
        return;
    }

    if (!ASSIGN_API.VALIDATE_SENT_MAILING || !ASSIGN_API.SEND_MAILING) {
        return;
    }

    async function fetchAlertedDirectorates() {
        const alertId = form.dataset.sendUrl.split('/').pop();
        const endpoint = `/directorate/list_alerted_directorates/${alertId}`;

        try {
            const response = await fetch(endpoint, { method: 'POST' });
            if (response.ok) {
                const directorates = await response.json();
                updateCheckboxes(directorates);
            } else {
                showToast('Erro ao buscar diretorias alertadas.', 'error');
            }
        } catch (err) {
            showToast('Erro ao buscar diretorias alertadas.', 'error');
        }
    }

    function updateCheckboxes(directorates) {
        const checkboxes = document.querySelectorAll('.checkbox-input');
        checkboxes.forEach(checkbox => {
            if (directorates.includes(checkbox.name)) {
                checkbox.checked = true;
            }
        });
    }

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

    async function sendMailing() {
        const selectedDirectorates = Array.from(document.querySelectorAll('.checkbox-input'))
            .filter(i => i.checked)
            .map(i => i.name);

        if (selectedDirectorates.length === 0) {
            showToast('Selecione pelo menos uma diretoria para enviar o mailing.', 'error');
            setLoading(false);
            return;
        }

        try {
            const response = await fetch(ASSIGN_API.SEND_MAILING, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ directorates: selectedDirectorates }),
            });

            if (!response.ok) {
                const errorText = await response.text();
                showToast(`Erro ao enviar mailing: ${errorText}`, 'error');
                return;
            }

            const data = await response.json();

            if (data.status === "error") {
                const errorText = data.error || 'Erro desconhecido.';
                showToast(`Erro ao enviar mailing: ${errorText}`, 'error');
            } else {
                showToast('Mailing enviado com sucesso!', 'success');
            }
        } catch (err) {
            showToast('Erro ao enviar mailing. Tente novamente mais tarde.', 'error');
        } finally {
            setLoading(false);
        }
    }

    function showModal(alertedDirectorates) {
        const modal = document.getElementById('mailingConfirmModal');
        const listContainer = document.getElementById('alertedDirectoratesListContainer');
        const listEl = document.getElementById('alertedDirectoratesList');
        const checkboxContainer = document.getElementById('confirmSendCheckboxContainer');
        const checkboxInput = document.getElementById('confirmSendCheckboxInput');
        const confirmBtn = document.getElementById('confirmSendBtn');

        if (!modal || !listEl || !confirmBtn) {
            return;
        }

        const list = Array.isArray(alertedDirectorates) ? alertedDirectorates : [];

        if (list.length > 0) {
            listEl.innerHTML = list.map(d => `<li>${d}</li>`).join('');
            listContainer.style.display = 'block';
            checkboxContainer.style.display = 'block';
            checkboxInput.checked = false;
            confirmBtn.disabled = true;

            checkboxInput.addEventListener('change', function () {
                confirmBtn.disabled = !this.checked;
            });
        } else {
            listContainer.style.display = 'none';
            listEl.innerHTML = '';
            checkboxContainer.style.display = 'none';
            confirmBtn.disabled = false;
        }

        modal.style.display = 'flex';

        confirmBtn.onclick = async function () {
            if (checkboxContainer.style.display !== 'none' && !checkboxInput.checked) {
                return;
            }
            modal.style.display = 'none';
            await sendMailing();
        };

        document.getElementById('cancelSendBtn').onclick = function () {
            modal.style.display = 'none';
            setLoading(false);
        };
    }

    async function validateSentMailing() {
        try {
            const response = await fetch(ASSIGN_API.VALIDATE_SENT_MAILING, { method: 'POST' });
            if (response.ok) {
                const data = await response.json();
                return data;
            } else {
                showToast('Erro ao validar envio anterior.', 'error');
                return null;
            }
        } catch (err) {
            showToast('Erro ao validar envio anterior.', 'error');
            return null;
        }
    }

    fetchAlertedDirectorates();

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const selectedDirectorates = Array.from(document.querySelectorAll('.checkbox-input'))
            .filter(i => i.checked)
            .map(i => i.name);

        if (selectedDirectorates.length === 0) {
            showToast('Selecione pelo menos uma diretoria para continuar.', 'error');
            return;
        }

        setLoading(true);
        const validationResult = await validateSentMailing();

        if (validationResult === null) {
            setLoading(false);
            return;
        }

        showModal(validationResult.alerted_directorates);
    });
});
