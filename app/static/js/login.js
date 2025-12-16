document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('loginForm');

    if (!form) {
        console.error('Formulário de login não encontrado.');
        return;
    }

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const email = form.email.value.trim();
        const password = form.password.value.trim();

        if (!email || !password) {
            showToast('Por favor, preencha todos os campos.', 'error');
            return;
        }

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: new URLSearchParams(new FormData(form)),
            });

            if (!response.ok) {
                const errorText = await response.text();
                console.error('Erro ao fazer login:', errorText);
                showToast('Erro ao fazer login. Verifique suas credenciais.', 'error');
                persistFormData(email, password);
                return;
            }

            const data = await response.json();
            if (data.status === 'error') {
                const errorMessage = data.message || 'Erro desconhecido.';
                console.error('Erro ao fazer login:', errorMessage);
                showToast(errorMessage, 'error');
                persistFormData(email, password);
            } else {
                showToast('Login realizado com sucesso!', 'success');
                window.location.href = data.redirect || '/';
            }
        } catch (err) {
            console.error('Erro inesperado ao fazer login:', err);
            showToast('Erro inesperado. Tente novamente mais tarde.', 'error');
            persistFormData(email, password);
        }
    });

    function persistFormData(email, password) {
        form.email.value = email;
        form.password.value = password;
    }

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
