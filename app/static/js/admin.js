document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('createUserForm');

    if (!form) {
        console.error('Formulário de criação de usuário não encontrado.');
        return;
    }

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const email = form.email.value.trim();
        const username = form.username.value.trim();
        const password = form.password.value.trim();
        const confirmPassword = form.confirm_password.value.trim();
        const role = form.role.value;

        if (!email || !username || !password || !confirmPassword || !role) {
            showToast('Todos os campos são obrigatórios.', 'error');
            return;
        }

        if (password !== confirmPassword) {
            showToast('As senhas não coincidem.', 'error');
            return;
        }

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, username, password, confirm_password: confirmPassword, role }),
            });

            const data = await response.json();

            if (response.ok && data.status === 'success') {
                showToast(data.message, 'success');
                form.reset();
            } else {
                showToast(data.message || 'Erro ao criar usuário.', 'error');
            }
        } catch (err) {
            console.error('Erro inesperado ao criar usuário:', err);
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
