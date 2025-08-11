document.addEventListener('DOMContentLoaded', function() {

    // --- Lógica para obter URLs dinâmicas do HTML ---
    const urlsDinamicas = document.getElementById('urls-dinamicas');
    const excluirVeiculoUrl = urlsDinamicas.dataset.excluirVeiculoUrl;
    const dashboardUrl = urlsDinamicas.dataset.dashboardUrl;

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

    // --- Lógica para o botão de exclusão da página de detalhes do Veículo ---
    const btnExcluirDetalhes = document.getElementById('btn-excluir-veiculo-detalhes');
    if (btnExcluirDetalhes) {
        btnExcluirDetalhes.addEventListener('click', function() {
            const veiculoId = this.dataset.id;
            if (confirm('Tem certeza que deseja excluir este veículo e todos os seus checklists?')) {
                const csrfToken = document.querySelector('form input[name="csrfmiddlewaretoken"]').value;
                
                fetch(excluirVeiculoUrl.replace('0', veiculoId), {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken
                    }
                })
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    }
                    throw new Error('Erro na resposta do servidor.');
                })
                .then(data => {
                    if (data.success) {
                        showToast(data.message, true);
                        setTimeout(() => window.location.href = dashboardUrl, 1500);
                    } else {
                        showToast('Erro ao excluir: ' + data.message, false);
                    }
                })
                .catch(error => {
                    console.error('Erro:', error);
                    showToast('Ocorreu um erro ao tentar excluir o veículo.', false);
                });
            }
        });
    }

});