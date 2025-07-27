document.addEventListener('DOMContentLoaded', function () {
    const chartData = document.getElementById('chart-data');
    const form = document.querySelector('form');

    const labels = JSON.parse(chartData.dataset.labels || '[]');

    const renderChart = (canvasId, label, data, color) => {
        const ctx = document.getElementById(canvasId);
        if (ctx && data.length) {
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: label,
                        data: data,
                        borderColor: color,
                        backgroundColor: 'transparent',
                        tension: 0.4,
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        }
    };


    if (document.getElementById('sugarChart')) {
        const sugarData = JSON.parse(chartData.dataset.sugar);
        renderChart('sugarChart', 'Blood Sugar (mmol/L)', sugarData, 'orange');
    }

    if (document.getElementById('pressureChart')) {
        const systolic = JSON.parse(chartData.dataset.systolic);
        const diastolic = JSON.parse(chartData.dataset.diastolic);
        const ctx = document.getElementById('pressureChart');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Systolic',
                        data: systolic,
                        borderColor: 'red',
                        backgroundColor: 'transparent',
                        tension: 0.4,
                    },
                    {
                        label: 'Diastolic',
                        data: diastolic,
                        borderColor: 'blue',
                        backgroundColor: 'transparent',
                        tension: 0.4,
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

    if (document.getElementById('pulseChart')) {
        const pulseData = JSON.parse(chartData.dataset.pulse);
        renderChart('pulseChart', 'Pulse (bpm)', pulseData, 'green');
    }

    // AJAX change form
    if (form) {
        form.addEventListener('change', function (e) {
            e.preventDefault();

            const params = new URLSearchParams(new FormData(form));
            fetch(`/charts/ajax/?${params.toString()}`)
                .then(response => response.json())
                .then(data => {
                    updateCharts(data);
                });
        });
    }
});

function updateCharts(data) {
    const labels = data.labels || [];

    // Blood Sugar
    if (Chart.getChart('sugarChart')) {
        Chart.getChart('sugarChart').destroy();
    }
    if (document.getElementById('sugarChart')) {
        if (data.sugar_values.length) {
            new Chart(document.getElementById('sugarChart'), {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Blood Sugar (mmol/L)',
                        data: data.sugar_values,
                        borderColor: 'orange',
                        tension: 0.4,
                    }]
                },
            });
        }
        const msg = document.getElementById('sugarNoData');
        if (msg) {
            msg.classList.toggle('d-none', data.sugar_values.length > 0);
        }
    }

    // Pressure
    if (Chart.getChart('pressureChart')) {
        Chart.getChart('pressureChart').destroy();
    }
    if (document.getElementById('pressureChart')) {
        const hasPressure = data.systolic.length || data.diastolic.length;
        if (hasPressure) {
            new Chart(document.getElementById('pressureChart'), {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Systolic',
                            data: data.systolic,
                            borderColor: 'red',
                            tension: 0.4,
                        },
                        {
                            label: 'Diastolic',
                            data: data.diastolic,
                            borderColor: 'blue',
                            tension: 0.4,
                        }
                    ]
                },
            });
        }
        const msg = document.getElementById('pressureNoData');
        if (msg) {
            msg.classList.toggle('d-none', hasPressure);
        }
    }

    // Pulse
    if (Chart.getChart('pulseChart')) {
        Chart.getChart('pulseChart').destroy();
    }
    if (document.getElementById('pulseChart')) {
        if (data.pulse.length) {
            new Chart(document.getElementById('pulseChart'), {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Pulse (bpm)',
                        data: data.pulse,
                        borderColor: 'green',
                        tension: 0.4,
                    }]
                },
            });
        }
        const msg = document.getElementById('pulseNoData');
        if (msg) {
            msg.classList.toggle('d-none', data.pulse.length > 0);
        }
    }
}
