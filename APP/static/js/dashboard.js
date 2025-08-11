document.addEventListener('DOMContentLoaded', function() {

    // --- Lógica para mensagens de feedback (Toasts) ---
    function showToast(message, isSuccess) {
        const toastContainer = document.querySelector('.toast-container');
        if (!toastContainer) {
            console.error('Toast container not found.');
            return;
        }

        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-bg-${isSuccess ? 'success' : 'danger'} border-0`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;
        toastContainer.appendChild(toast);
        const bootstrapToast = new bootstrap.Toast(toast);
        bootstrapToast.show();
    }

    // --- Lógica do pop-up de alerta ---
    const checklistsVencidosSpan = document.getElementById('checklists-vencidos');
    const checklistsAVencerSpan = document.getElementById('checklists-a-vencer');
    
    if (checklistsVencidosSpan) {
        const checklistsVencidos = parseInt(checklistsVencidosSpan.innerText.trim());
        const checklistsAVencer = parseInt(checklistsAVencerSpan.innerText.trim());
        if (checklistsVencidos > 0 || checklistsAVencer > 0) {
            document.getElementById('alerta-popup').style.display = 'block';
        }
    }

    // --- Lógica para envio de formulários via AJAX ---
    function submitAjaxForm(event, successMessage) {
        event.preventDefault();

        const form = event.target;
        const formData = new FormData(form);
        const csrfToken = formData.get('csrfmiddlewaretoken');
        
        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else if (response.status === 302) { // Não processa JSON, deixa o navegador seguir o redirect
                return;
            }
            throw new Error('Erro na resposta do servidor.');
        })
        .then(data => {
            if (data && data.success) { // Verifica se há dados e se o sucesso é verdadeiro
                showToast(successMessage, true);
                setTimeout(() => window.location.reload(), 1500);
            } else if (data) {
                let errorMessage = 'Erro no formulário. Verifique os dados.';
                if (data.errors) {
                    errorMessage += '\n' + JSON.stringify(data.errors);
                } else if (data.message) {
                    errorMessage = data.message;
                }
                showToast(errorMessage, false);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            showToast('Ocorreu um erro ao tentar enviar o formulário.', false);
        });
    }

    // --- Anexar a função de envio a todos os formulários ---
    const formVeiculo = document.getElementById('form-veiculo');
    if (formVeiculo) {
        formVeiculo.addEventListener('submit', (e) => submitAjaxForm(e, 'Veículo cadastrado/atualizado com sucesso!'));
    }

    const formGR = document.getElementById('form-gr');
    if (formGR) {
        formGR.addEventListener('submit', (e) => submitAjaxForm(e, 'Gerenciadora de Risco cadastrada/atualizada com sucesso!'));
    }

    const formChecklist = document.getElementById('form-checklist');
    if (formChecklist) {
        formChecklist.addEventListener('submit', (e) => submitAjaxForm(e, 'Checklist cadastrado/atualizado com sucesso!'));
    }

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            fetch(e.target.action, {
                method: 'POST',
                body: formData,
                headers: {'X-CSRFToken': formData.get('csrfmiddlewaretoken')}
            }).then(response => {
                if (response.ok) { // Redirecionamento é um sucesso
                    showToast('Login realizado com sucesso!', true);
                    setTimeout(() => window.location.reload(), 1500);
                } else {
                    showToast('Usuário ou senha inválidos.', false);
                }
            }).catch(error => {
                console.error('Erro:', error);
                showToast('Ocorreu um erro de rede.', false);
            });
        });
    }
    
    const logoutForm = document.getElementById('logout-form');
    if (logoutForm) {
        logoutForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            fetch(e.target.action, {
                method: 'POST',
                body: formData,
                headers: {'X-CSRFToken': formData.get('csrfmiddlewaretoken')}
            }).then(response => {
                if (response.ok) {
                    showToast('Logout realizado com sucesso!', true);
                    setTimeout(() => window.location.reload(), 1500);
                } else {
                    showToast('Ocorreu um erro ao sair.', false);
                }
            }).catch(error => {
                console.error('Erro:', error);
                showToast('Ocorreu um erro de rede.', false);
            });
        });
    }

});