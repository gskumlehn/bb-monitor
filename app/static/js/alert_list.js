document.addEventListener('DOMContentLoaded', () => {
    const filterForm = document.getElementById('filterForm');
    const alertTableContainer = document.getElementById('alertTableContainer');
    const alertTableBody = document.querySelector('#alertTable tbody');
    const baseUrlInput = document.getElementById('baseUrl');
    const baseUrl = baseUrlInput ? baseUrlInput.value : '';
    const exportCsvButton = document.getElementById('exportCsvButton');

    const now = new Date();
    const currentMonth = now.getMonth() + 1;
    const currentYear = now.getFullYear();

    const monthSelect = document.getElementById('month');
    const yearInput = document.getElementById('year');

    if (monthSelect) monthSelect.value = currentMonth;
    if (yearInput) yearInput.value = currentYear;

    if (filterForm) {
        filterForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const month = monthSelect.value.trim();
            const year = yearInput.value.trim();

            if (!month || !year) {
                alert('Por favor, preencha o mês e o ano.');
                return;
            }

            alertTableBody.innerHTML = '';
            alertTableContainer.style.display = 'none';

            try {
                const response = await fetch(`/alert/list?month=${month}&year=${year}`);
                if (!response.ok) {
                    throw new Error('Falha na requisição');
                }

                const alerts = await response.json();
                alertTableBody.innerHTML = '';

                if (alerts && alerts.length > 0) {
                    alerts.forEach(alert => {
                        const row = document.createElement('tr');

                        let dateStr = '-';
                        if (alert.delivery_datetime) {
                            try {
                                const dateObj = new Date(alert.delivery_datetime);
                                const day = String(dateObj.getDate()).padStart(2, '0');
                                const month = String(dateObj.getMonth() + 1).padStart(2, '0');
                                const year = dateObj.getFullYear();
                                const hours = String(dateObj.getHours()).padStart(2, '0');
                                const minutes = String(dateObj.getMinutes()).padStart(2, '0');

                                dateStr = `${day}/${month}/${year}<br>${hours}:${minutes}`;
                            } catch (e) {
                                dateStr = alert.delivery_datetime;
                            }
                        }

                        let statusStr = alert.mailing_status || '-';
                        if (statusStr === 'SIM') {
                            statusStr = 'Whats Enviado';
                        } else if (statusStr === 'NÃO') {
                            statusStr = 'Não Enviado';
                        }

                        row.innerHTML = `
                            <td style="text-align: center;">${dateStr}</td>
                            <td style="text-align: center;">${alert.sequential_code || '-'}</td>
                            <td>${alert.title || '-'}</td>
                            <td>${statusStr}</td>
                            <td style="text-align: center;">${alert.criticality_level || '-'}</td>
                            <td data-id="${alert.id}">
                                <div class="btn-action-container">
                                    <a href="${baseUrl}/email/render/${alert.id}" target="_blank" class="btn btn-sm" style="padding: 6px 12px; background-color: var(--bb-blue); color: white; border: none; border-radius: 4px; cursor: pointer; display: inline-flex; align-items: center; justify-content: center; margin-right: 5px;" title="Ver Email">
                                        <svg class="icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                            <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                                            <polyline points="22,6 12,13 2,6"></polyline>
                                        </svg>
                                    </a>
                                    <a href="${baseUrl}/directorate/alert/${alert.id}" class="btn btn-sm" style="padding: 6px 12px; background-color: #ef4444; color: white; border: none; border-radius: 4px; cursor: pointer; display: inline-flex; align-items: center; justify-content: center;" title="Alertar Diretorias">
                                        <svg class="icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                            <path d="M12 2L2 22h20L12 2z"></path>
                                            <path d="M12 8v6"></path>
                                            <path d="M12 18h.01"></path>
                                        </svg>
                                    </a>
                                </div>
                            </td>
                        `;
                        alertTableBody.appendChild(row);
                    });
                    alertTableContainer.style.display = 'block';
                } else {
                    alertTableContainer.style.display = 'none';
                    alert('Nenhum alerta encontrado para o período selecionado.');
                }
            } catch (error) {
                console.error(error);
                alert('Erro ao buscar alertas. Verifique o console para mais detalhes.');
            }
        });
    }

    if (exportCsvButton) {
        exportCsvButton.addEventListener('click', () => {
            const rows = Array.from(alertTableBody.querySelectorAll('tr'));
            if (rows.length === 0) {
                alert('Nenhum dado para exportar.');
                return;
            }

            const month = monthSelect.value.trim();
            const year = yearInput.value.trim();
            const fileName = `alertas-bb-${month}-${year}.csv`;

            const csvContent = [];
            csvContent.push(['Data de Entrega', 'Código', 'Título', 'Status', 'Nível de Criticidade', 'Id', 'Links'].join(','));

            rows.forEach(row => {
                const cells = Array.from(row.querySelectorAll('td'));

                if (cells.length < 6) return;

                const rowData = [];
                let dateText = cells[0].innerHTML.replace('<br>', ' ').trim();
                rowData.push(`"${dateText}"`);

                rowData.push(`"${cells[1].textContent.trim()}"`);
                rowData.push(`"${cells[2].textContent.trim()}"`);
                rowData.push(`"${cells[3].textContent.trim()}"`);
                rowData.push(`"${cells[4].textContent.trim()}"`);

                const actionsCell = cells[5];
                const id = actionsCell.getAttribute('data-id') || '';
                rowData.push(`"${id}"`);

                const emailLink = actionsCell.querySelector('a[title="Ver Email"]');
                const linkUrl = emailLink ? emailLink.getAttribute('href') : '';
                rowData.push(`"${linkUrl}"`);

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
    }
});
