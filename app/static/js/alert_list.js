document.addEventListener('DOMContentLoaded', () => {
    const filterForm = document.getElementById('filterForm');
    const alertTableContainer = document.getElementById('alertTableContainer');
    const alertTableBody = document.querySelector('#alertTable tbody');
    const baseUrl = document.getElementById('baseUrl').value;
    const exportCsvButton = document.getElementById('exportCsvButton');

    const now = new Date();
    const currentMonth = now.getMonth() + 1;
    const currentYear = now.getFullYear();
    document.getElementById('month').value = currentMonth;
    document.getElementById('year').value = currentYear;

    filterForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const month = document.getElementById('month').value.trim();
        const year = document.getElementById('year').value.trim();

        if (!month || !year) {
            alert('Por favor, preencha o mês e o ano.');
            return;
        }

        alertTableBody.innerHTML = '';
        alertTableContainer.style.display = 'none';

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
                    row.innerHTML = `
                        <td>${new Date(alert.delivery_datetime).toLocaleString('pt-BR')}</td>
                        <td>${alert.sequential_code}</td>
                        <td>${alert.title}</td>
                        <td>${alert.mailing_status}</td>
                        <td>${alert.criticality_level}</td>
                        <td>${alert.id}</td>
                        <td><a href="${baseUrl}/email/render/${alert.id}">link</a></td>
                    `;
                    alertTableBody.appendChild(row);
                });
                alertTableContainer.style.display = 'block';
            } else {
                alertTableContainer.style.display = 'none';
                alert('Nenhum alerta encontrado para o período selecionado.');
            }
        } catch (error) {
            alert('Erro ao buscar alertas.');
        }
    });

    exportCsvButton.addEventListener('click', () => {
        const rows = Array.from(alertTableBody.querySelectorAll('tr'));
        if (rows.length === 0) {
            alert('Nenhum dado para exportar.');
            return;
        }

        const month = document.getElementById('month').value.trim();
        const year = document.getElementById('year').value.trim();
        const fileName = `alertas-bb-${month}-${year}.csv`;

        const csvContent = [];
        csvContent.push(['Data de Entrega', 'Código', 'Título', 'Status', 'Nível de Criticidade', 'Id', 'Link'].join(','));

        rows.forEach(row => {
            const cells = Array.from(row.querySelectorAll('td'));
            const rowData = cells.map((cell, index) => {
                if (index === 6) {
                    const link = cell.querySelector('a');
                    return link ? `"${link.getAttribute('href')}"` : '""';
                }
                return `"${cell.textContent.trim()}"`;
            });
            csvContent.push(rowData.join(','));
        });

        const csvBlob = new Blob([csvContent.join('\n')], { type: 'text/csv;charset=utf-8;' });
        const csvUrl = URL.createObjectURL(csvBlob);
        const downloadLink = document.createElement('a');
        downloadLink.href = csvUrl;
        downloadLink.download = fileName;
        downloadLink.style.display = 'none';
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
    });
});
