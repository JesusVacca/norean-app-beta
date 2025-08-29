window.addEventListener('DOMContentLoaded',function (){

    const rolesScript = document.getElementById('roles-data');
    const furnituresScript = document.getElementById('furnitures-data');

    if (!rolesScript || !furnituresScript) {
        console.log("No se encontró el JSON script en el DOM");
        return;
    }

    // Obtener datos desde el template
    const roles = JSON.parse(rolesScript.textContent);
    const furnitures = JSON.parse(furnituresScript.textContent);


    // Mapear labels y counts
    const rolesLabels = roles.map(r => r.name);
    const rolesCounts = roles.map(r => r.count);

    const furnituresLabels = furnitures.map(f => f.status);
    const furnituresCounts = furnitures.map(f => f.count);

    // Colores y opciones comunes
    const chartColors = [
        'rgba(54, 162, 235, 0.6)',
        'rgba(255, 206, 86, 0.6)',
        'rgba(255, 99, 132, 0.6)',
        'rgba(75, 192, 192, 0.6)',
        'rgba(2,48,80,0.6)',
    ];

    const chartOptions = {
        responsive: true,
        plugins: {
                legend: { display: true, position: 'top', align: 'start', labels: { boxWidth: 20, padding: 15, font: { size: 14, weight: 'bold' } } },
                tooltip: { enabled: true }
        }
    };

    // Función genérica para crear gráficos
    function createChart(elementId, labels, counts, type, label) {
        new Chart(document.getElementById(elementId).getContext('2d'), {
            type: type,
            data: { labels: labels, datasets: [{ label: label, data: counts, backgroundColor: chartColors, borderWidth: 1 }] },
            options: chartOptions
        });
    }

    // Crear gráficos
    createChart('rolesGraph', rolesLabels, rolesCounts, 'doughnut', 'Usuarios por Rol');
    createChart('furnitureGraph', furnituresLabels, furnituresCounts, 'pie', 'Mobiliarios por estado');

})