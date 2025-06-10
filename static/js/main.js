document.addEventListener('DOMContentLoaded', function() {
    // Manejo de selección visual
    document.querySelectorAll('.interes-img').forEach(img => {
        img.addEventListener('click', () => {
            img.classList.toggle('selected');
        });
    });

    document.getElementById('enviar').addEventListener('click', () => {
        // Construir el mapa: {seccion: [intereses seleccionados]}
        const seleccion = {};
        document.querySelectorAll('.interes-img.selected').forEach(img => {
            const seccion = img.getAttribute('data-seccion');
            const interes = img.getAttribute('data-interes');
            if (!seleccion[seccion]) {
                seleccion[seccion] = [];
            }
            seleccion[seccion].push(interes);
        });
        console.log(seleccion);
        if (Object.keys(seleccion).length === 0) {
            alert('Selecciona al menos un interés.');
            return;
        }

        fetch('/api/recomendar', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(seleccion)
        })
        .then(res => res.json())
        .then(data => {
            mostrarResultados(data.lugares);
        });
    });

    function mostrarResultados(lugares) {
        const div = document.getElementById('resultados');
        div.innerHTML = '';
        if (!lugares || lugares.length === 0) {
            div.innerHTML = '<p style="text-align:center;color:#888;">No se encontraron lugares recomendados.</p>';
            return;
        }
        div.innerHTML = lugares.map(lugar => `
            <div class="lugar-card">
                <img class="lugar-img" src="${lugar.imagen || ''}" alt="${lugar.nombre}">
                <div class="lugar-info">
                    <h3>${lugar.nombre}</h3>
                    <span>${lugar.descripcion}</span>
                </div>
            </div>
        `).join('');
    }
});