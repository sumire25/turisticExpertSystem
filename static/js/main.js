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
            mostrarResultados(data.recomendaciones);
        });
    });

    function mostrarResultados(recomendaciones) {
        const div = document.getElementById('resultados');
        div.innerHTML = '';
        if (!recomendaciones || recomendaciones.length === 0) {
            div.innerHTML = '<p style="text-align:center;color:#888;">No se encontraron lugares recomendados.</p>';
            return;
        }
        div.innerHTML = recomendaciones.map(lugar => `
            <div class="lugar-card">
                <div class="lugar-info">
                    <h3>${lugar.nombre} (${lugar.departamento})</h3>
                    <span>${lugar.descripcion_detallada}</span><br>
                    <b>Puntuación:</b> ${lugar.puntuacion}<br>
                    <b>Regiones:</b> ${lugar.regiones.join(', ')}<br>
                    <b>Climas ideales:</b> ${lugar.climas_ideal.join(', ')}<br>
                    <b>Accesibilidad:</b> ${lugar.accesibilidad_texto}<br>
                    <b>Presupuesto:</b> ${lugar.presupuesto_requerido.join(', ')}<br>
                    <b>Explicaciones:</b> ${lugar.explicaciones.join('; ')}
                </div>
            </div>
        `).join('');
    }
});