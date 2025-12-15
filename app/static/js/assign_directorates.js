function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    if (!toast) {
        console.error('Elemento de toast não encontrado.');
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
        console.error('Formulário assignForm não encontrado.');
        return;
    }

    if (!ASSIGN_API.VALIDATE_SENT_MAILING || !ASSIGN_API.SEND_MAILING) {
        console.error('URLs de validação ou envio não definidas no formulário.');
        return;
    }

    async function fetchAlertedDirectorates() {
        const alertId = form.dataset.sendUrl.split('/').pop(); // Extrair alert_id da URL
        const endpoint = `/directorate/list_alerted_directorates/${alertId}`;

        try {
            const response = await fetch(endpoint, { method: 'POST' });
            if (response.ok) {
                const directorates = await response.json();
                updateCheckboxes(directorates);
            } else {
                console.error('Erro ao buscar diretorias alertadas:', await response.text());
            }
        } catch (err) {
            console.error('Erro ao buscar diretorias alertadas:', err);
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
                console.error('Erro ao enviar mailing:', errorText);
                showToast(`Erro ao enviar mailing: ${errorText}`, 'error');
                return;
            }

            const data = await response.json();

            if (data.status === "error") {
                const errorText = data.error || 'Erro desconhecido.';
                console.error('Erro ao enviar mailing:', errorText);
                showToast(`Erro ao enviar mailing: ${errorText}`, 'error');
            } else {
                showToast('Mailing enviado com sucesso!', 'success');
            }
        } catch (err) {
            console.error('Erro ao enviar mailing:', err);
            showToast('Erro ao enviar mailing. Tente novamente mais tarde.', 'error');
        } finally {
            setLoading(false); // Garantir que o botão volte ao estado normal
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
            console.warn('Elementos da modal não encontrados.');
            return;
        }

        const list = Array.isArray(alertedDirectorates) ? alertedDirectorates : [];

        // Preencher a lista de diretorias alertadas, se houver
        if (list.length > 0) {
            listEl.innerHTML = list.map(d => `<li>${d}</li>`).join('');
            listContainer.style.display = 'block';
            checkboxContainer.style.display = 'block';
            checkboxInput.checked = false;
            confirmBtn.disabled = true;

            // Adicionar evento para habilitar o botão de confirmação
            checkboxInput.addEventListener('change', function () {
                confirmBtn.disabled = !this.checked;
            });
        } else {
            // Caso não haja diretorias alertadas, esconder lista e checkbox
            listContainer.style.display = 'none';
            listEl.innerHTML = '';
            checkboxContainer.style.display = 'none';
            confirmBtn.disabled = false;
        }

        // Mostrar a modal
        modal.style.display = 'flex';

        // Configurar o botão de confirmação
        confirmBtn.onclick = async function () {
            if (checkboxContainer.style.display !== 'none' && !checkboxInput.checked) {
                return;
            }
            modal.style.display = 'none';
            await sendMailing();
        };

        // Configurar o botão de cancelamento
        document.getElementById('cancelSendBtn').onclick = function () {
            modal.style.display = 'none';
            setLoading(false); // Garantir que o botão volte ao estado normal
        };
    }

    async function validateSentMailing() {
        try {
            const response = await fetch(ASSIGN_API.VALIDATE_SENT_MAILING, { method: 'POST' });
            if (response.ok) {
                const data = await response.json();
                return data;
            } else {
                const errorText = await response.text();
                console.error('Erro ao validar envio anterior:', errorText);
                showToast('Erro ao validar envio anterior.', 'error');
                return null;
            }
        } catch (err) {
            console.error('Erro ao validar envio anterior:', err);
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
