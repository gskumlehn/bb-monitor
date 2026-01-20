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

    let alreadyAlertedDirectorates = [];

    async function fetchDirectoratesData() {
        const alertId = form.dataset.sendUrl.split('/').pop();
        const endpoint = `/directorate/list_alerted_directorates/${alertId}`;

        try {
            const response = await fetch(endpoint, { method: 'POST' });
            if (response.ok) {
                const data = await response.json();

                alreadyAlertedDirectorates = data.alerted || [];
                updateCheckboxes(data.suggested || [], data.alerted || []);
            } else {
                showToast('Erro ao buscar dados das diretorias.', 'error');
            }
        } catch (err) {
            showToast('Erro ao buscar dados das diretorias.', 'error');
        }
    }

    function updateCheckboxes(suggested, alerted) {
        const checkboxes = document.querySelectorAll('.checkbox-input');
        checkboxes.forEach(checkbox => {
            const name = checkbox.name;

            checkbox.checked = false;
            checkbox.disabled = false;
            const label = document.querySelector(`label[for="${checkbox.id}"]`);
            if (label) {
                label.classList.remove('disabled');
                label.style.backgroundColor = '';
                label.style.color = '';
                label.style.cursor = '';
                label.style.borderColor = '';
            }

            if (alerted.includes(name)) {
                checkbox.checked = true;
                checkbox.disabled = true;
                if (label) {
                    label.classList.add('disabled');
                    label.style.backgroundColor = '#e0e0e0';
                    label.style.color = '#888';
                    label.style.cursor = 'not-allowed';
                    label.style.borderColor = '#ccc';
                }
            }
            else if (suggested.includes(name)) {
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
            .filter(i => i.checked && !i.disabled)
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
                fetchDirectoratesData();
            }
        } catch (err) {
            showToast('Erro ao enviar mailing. Tente novamente mais tarde.', 'error');
        } finally {
            setLoading(false);
        }
    }

    function showModal(newDirectorates) {
        const modal = document.getElementById('mailingConfirmModal');

        const alertedListContainer = document.getElementById('alertedDirectoratesListContainer');
        const alertedListEl = document.getElementById('alertedDirectoratesList');

        const newListContainer = document.getElementById('newDirectoratesListContainer');
        const newListEl = document.getElementById('newDirectoratesList');

        const checkboxContainer = document.getElementById('confirmSendCheckboxContainer');
        const checkboxInput = document.getElementById('confirmSendCheckboxInput');
        const confirmBtn = document.getElementById('confirmSendBtn');

        if (!modal || !alertedListEl || !newListEl || !confirmBtn) {
            return;
        }

        if (newDirectorates && newDirectorates.length > 0) {
            const labels = newDirectorates.map(name => {
                const cb = document.querySelector(`.checkbox-input[name="${name}"]`);
                const label = document.querySelector(`label[for="${cb.id}"]`);
                return label ? label.textContent : name;
            });

            newListEl.innerHTML = labels.map(d => `<li>${d}</li>`).join('');
            newListContainer.style.display = 'block';
        } else {
            newListContainer.style.display = 'none';
        }

        if (alreadyAlertedDirectorates.length > 0) {
            const labels = alreadyAlertedDirectorates.map(name => {
                const cb = document.querySelector(`.checkbox-input[name="${name}"]`);
                if (cb) {
                    const label = document.querySelector(`label[for="${cb.id}"]`);
                    return label ? label.textContent : name;
                }
                return name;
            });

            alertedListEl.innerHTML = labels.map(d => `<li>${d}</li>`).join('');
            alertedListContainer.style.display = 'block';

            checkboxContainer.style.display = 'block';
            checkboxInput.checked = false;
            confirmBtn.disabled = true;

            checkboxInput.onchange = function() {
                confirmBtn.disabled = !this.checked;
            };
        } else {
            alertedListContainer.style.display = 'none';
            alertedListEl.innerHTML = '';

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

    fetchDirectoratesData();

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const selectedDirectorates = Array.from(document.querySelectorAll('.checkbox-input'))
            .filter(i => i.checked && !i.disabled)
            .map(i => i.name);

        if (selectedDirectorates.length === 0) {
            showToast('Selecione pelo menos uma diretoria para continuar.', 'error');
            return;
        }

        setLoading(true);

        showModal(selectedDirectorates);
    });
});
