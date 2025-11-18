document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.checkbox-btn').forEach(function (lbl) {
        lbl.addEventListener('click', function (e) {
            e.preventDefault();
            const forId = this.getAttribute('for') || this.htmlFor;
            if (!forId) return;
            const cb = document.getElementById(forId);
            if (!cb) return;
            cb.checked = !cb.checked;
            cb.value = cb.checked ? "true" : "false";
            if (cb.checked) {
                this.classList.add('cb-checked');
            } else {
                this.classList.remove('cb-checked');
            }
            cb.dispatchEvent(new Event('change', { bubbles: true }));
            cb.focus();
        });
    });

    document.querySelectorAll('.checkbox-input').forEach(function (cb) {
        const lbl = document.querySelector('label[for="' + cb.id + '"]');
        if (lbl) {
            if (cb.checked) lbl.classList.add('cb-checked');
            else lbl.classList.remove('cb-checked');
        }
        cb.addEventListener('change', function () {
            cb.value = cb.checked ? "true" : "false";
            if (lbl) {
                if (cb.checked) lbl.classList.add('cb-checked');
                else lbl.classList.remove('cb-checked');
            }
        });
    });

    const form = document.getElementById('assignForm');
    const submitBtn = document.getElementById('submitBtn');

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

    if (form) {
        form.addEventListener('submit', async function (e) {
            e.preventDefault();
            const chosen = Array.from(document.querySelectorAll('.checkbox-input'))
                .filter(i => i.value === "true")
                .map(i => i.name);

            if (chosen.length === 0) {
                showToast('Selecione pelo menos uma diretoria para enviar o mailing.', 'error');
                return;
            }

            const url = form.getAttribute('action');

            setLoading(true);
            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ directorates: chosen }),
                });

                if (response.ok) {
                    const result = await response.json();
                    handleMailingResponse(result);
                } else {
                    const error = await response.json();
                    showToast(error.description || 'Erro ao enviar mailing. Entre em contato com o atendimento.', 'error');
                }
            } catch (err) {
                showToast('Erro ao enviar mailing. Entre em contato com o atendimento.', 'error');
                console.error('Erro ao enviar mailing:', err);
            } finally {
                setLoading(false);
            }
        });
    }

    function handleMailingResponse(result) {
        const errors = result.results.filter(r => r.status === 'error');
        if (errors.length === result.results.length) {
            showToast('Erro ao enviar mailing. Entre em contato com o atendimento.', 'error');
        } else if (errors.length > 0) {
            const errorDirectorates = errors.map(e => e.directorate).join(', ');
            showToast(`Erro ao enviar para as seguintes diretorias: ${errorDirectorates}. Entre em contato com o atendimento.`, 'error');
        } else {
            showToast('Mailing enviado com sucesso!', 'success');
        }
    }

    function showToast(message, type = 'success') {
        const toast = document.getElementById('toast');
        if (!toast) return;

        toast.textContent = message;
        toast.className = `toast ${type} show`;

        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }
});
