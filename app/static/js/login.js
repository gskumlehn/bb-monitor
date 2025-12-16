document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('loginForm');
    const forgotPasswordTrigger = document.getElementById('forgotPasswordTrigger');
    const forgotPasswordModal = document.getElementById('forgotPasswordModal');
    const confirmForgotPasswordBtn = document.getElementById('confirmForgotPasswordBtn');
    const cancelForgotPasswordBtn = document.getElementById('cancelForgotPasswordBtn');
    const forgotPasswordEmail = document.getElementById('forgotPasswordEmail');

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

    if (forgotPasswordTrigger) {
        forgotPasswordTrigger.addEventListener('click', function (e) {
            e.preventDefault();
            forgotPasswordModal.style.display = 'flex';
        });
    }

    if (cancelForgotPasswordBtn) {
        cancelForgotPasswordBtn.addEventListener('click', function () {
            forgotPasswordModal.style.display = 'none';
        });
    }

    if (confirmForgotPasswordBtn) {
        confirmForgotPasswordBtn.addEventListener('click', async function () {
            const email = forgotPasswordEmail.value.trim();

            if (!email) {
                showToast('Por favor, insira seu email antes de confirmar.', 'error');
                return;
            }

            try {
                const response = await fetch('/auth/forgot_password', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: new URLSearchParams({ email }),
                });

                if (!response.ok) {
                    const errorText = await response.text();
                    console.error('Erro ao enviar email de redefinição:', errorText);
                    showToast('Erro ao enviar email. Tente novamente mais tarde.', 'error');
                    return;
                }

                const data = await response.json();
                if (data.status === 'success') {
                    showToast('Email enviado com sucesso!', 'success');
                    forgotPasswordModal.style.display = 'none';
                } else {
                    showToast(data.message || 'Erro desconhecido.', 'error');
                }
            } catch (err) {
                console.error('Erro inesperado ao enviar email:', err);
                showToast('Erro inesperado. Tente novamente mais tarde.', 'error');
            }
        });
    }

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

    // Modal close functionality
    document.querySelectorAll('[data-dismiss="modal"]').forEach((closeButton) => {
        closeButton.addEventListener('click', () => {
            forgotPasswordModal.style.display = 'none';
        });
    });
});
