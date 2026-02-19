(function () {
    const canvas = document.getElementById('adminAppsChart');
    if (!canvas || typeof Chart === 'undefined') {
        return;
    }

    const labels = (canvas.dataset.labels || '')
        .split('|')
        .map((item) => item.trim())
        .filter(Boolean);

    const counts = (canvas.dataset.counts || '')
        .split(',')
        .map((item) => Number(item.trim()) || 0);

    if (!labels.length || !counts.length) {
        return;
    }

    const ctx = canvas.getContext('2d');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels,
            datasets: [
                {
                    label: 'Models per app',
                    data: counts,
                    borderColor: '#2563eb',
                    backgroundColor: 'rgba(37, 99, 235, 0.15)',
                    fill: true,
                    tension: 0.38,
                    pointBackgroundColor: '#1d4ed8',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 2,
                    pointRadius: 4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: '#0f172a',
                    titleColor: '#ffffff',
                    bodyColor: '#e2e8f0',
                    padding: 12
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(148, 163, 184, 0.25)'
                    },
                    ticks: {
                        precision: 0,
                        color: '#475569'
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#475569'
                    }
                }
            }
        }
    });
})();
