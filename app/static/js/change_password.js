document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('changePasswordForm');

    if (!form) {
        console.error('Formulário de alteração de senha não encontrado.');
        return;
    }

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const currentPassword = form.current_password.value.trim();
        const newPassword = form.new_password.value.trim();
        const confirmNewPassword = form.confirm_new_password.value.trim();

        if (!currentPassword || !newPassword || !confirmNewPassword) {
            showToast('Todos os campos são obrigatórios.', 'error');
            return;
        }

        if (newPassword !== confirmNewPassword) {
            showToast('As novas senhas não coincidem.', 'error');
            return;
        }

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ current_password: currentPassword, new_password: newPassword }),
            });

            const data = await response.json();

            if (response.ok && data.status === 'success') {
                showToast(data.message, 'success');
                form.reset();
            } else {
                showToast(data.message || 'Erro ao alterar senha.', 'error');
            }
        } catch (err) {
            console.error('Erro inesperado ao alterar senha:', err);
            showToast('Erro inesperado. Tente novamente mais tarde.', 'error');
        }
    });

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
});

