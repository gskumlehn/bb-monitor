document.addEventListener('DOMContentLoaded', () => {
    const filterForm = document.getElementById('filterForm');
    const alertTableContainer = document.getElementById('alertTableContainer');
    const alertTableBody = document.querySelector('#alertTable tbody');

    filterForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const month = document.getElementById('month').value.trim();
        const year = document.getElementById('year').value.trim();

        if (!month || !year) {
            alert('Por favor, preencha o mês e o ano.');
            return;
        }

        try {
            const response = await fetch(`/alert/list?month=${month}&year=${year}`);
            if (!response.ok) {
                alert('Erro ao buscar alertas.');
                return;
            }

            const alerts = await response.json();
            alertTableBody.innerHTML = '';

            if (alerts.length > 0) {
                alerts.forEach(alert => {
                    const row = document.createElement('tr');
                    row.classList.add('clickable-row');
                    row.dataset.alertId = alert.id;
                    row.innerHTML = `
                        <td>${new Date(alert.delivery_datetime).toLocaleString('pt-BR')}</td>
                        <td>${alert.title}</td>
                        <td>${alert.mailing_status}</td>
                        <td>${alert.criticality_level}</td>
                        <td>${alert.id}</td>
                    `;
                    alertTableBody.appendChild(row);
                });
                alertTableContainer.style.display = 'block';

                // Add click event to rows
                document.querySelectorAll('.clickable-row').forEach(row => {
                    row.addEventListener('click', () => {
                        const alertId = row.dataset.alertId;
                        window.location.href = `/email/render/${alertId}`;
                    });
                });
            } else {
                alertTableContainer.style.display = 'none';
                alert('Nenhum alerta encontrado para o período selecionado.');
            }
        } catch (error) {
            console.error('Erro ao buscar alertas:', error);
            alert('Erro ao buscar alertas.');
        }
    });
});
