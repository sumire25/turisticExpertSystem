from flask import Flask, render_template, request, jsonify, url_for
from expert_system.knowledge_base import lugares_turisticos_peru
from expert_system.inference_engine import recomendar_lugares

app = Flask(__name__)

# --- FRONTEND: rutas para mostrar páginas ---
@app.route('/')
def index():
    image_map = {
        "Lima": url_for('static', filename='img/lima.jpg'),
        "Cusco": url_for('static', filename='img/cusco.jpg'),
        "Arequipa": url_for('static', filename='img/arequipa.jpg'),
        "Iquitos": url_for('static', filename='img/iquitos.jpg'),
        "Trujillo": url_for('static', filename='img/trujillo.jpg'),
        "Puno": url_for('static', filename='img/puno.jpg'),
        "Nazca": url_for('static', filename='img/nazca.jpg'),
        "Chachapoyas": url_for('static', filename='img/chachapoyas.jpg'),
        "Huaraz": url_for('static', filename='img/huaraz.jpg'),
        "Tarapoto": url_for('static', filename='img/tarapoto.jpg'),
        "Puerto Maldonado": url_for('static', filename='img/puerto_maldonado.jpg'),
        "Tumbes": url_for('static', filename='img/tumbes.jpg'),
        "Ica": url_for('static', filename='img/ica.jpg'),
        "Cajamarca": url_for('static', filename='img/cajamarca.jpg'),
        "Piura": url_for('static', filename='img/piura.jpg'),
        "Ayacucho": url_for('static', filename='img/ayacucho.jpg'),
        "Andahuaylas": url_for('static', filename='img/andahuaylas.jpg'),
        "La Mar (Ayacucho)": url_for('static', filename='img/la_mar.jpg'),
        "Pichari (VRAEM)": url_for('static', filename='img/pichari.jpg')
    }
    return render_template('index.html', image_map=image_map)


@app.route('/resultado', methods=['POST'])
def resultado():
    # Aquí puedes simular datos o dejarlo vacío por ahora
    intereses = request.form.get('intereses', '')
    lugares = []
    return render_template('resultado.html', intereses=intereses, lugares=lugares)

# --- BACKEND: API para lógica de recomendación ---
@app.route('/api/recomendar', methods=['POST'])
def obtener_recomendaciones():
    # Verifica que el tipo de contenido de la solicitud sea JSON
    if not request.is_json:
        return jsonify({"error": "La solicitud debe ser JSON"}), 400

    # Obtiene el JSON enviado por el cliente (la memoria de trabajo)
    memoria_de_trabajo = request.get_json()

    # Registra las preferencias recibidas para depuración (opcional)
    print(f"Preferencias recibidas: {memoria_de_trabajo}")

    # Llama al mecanismo de inferencia para obtener las recomendaciones
    resultados_raw = recomendar_lugares(memoria_de_trabajo)

    # Prepara los resultados para ser enviados como JSON al frontend
    recomendaciones_para_json = []
    if resultados_raw:
        for item in resultados_raw:
            recomendaciones_para_json.append({
                "nombre": item["lugar"]["nombre"],
                "departamento": item["lugar"]["departamento"],
                "descripcion_detallada": item["lugar"]["descripcion_detallada"], # La descripción específica para el usuario
                "puntuacion": item["puntuacion"], # La puntuación de relevancia del sistema
                "explicaciones": item["explicaciones"], # Las razones del porqué (componente explicativo)
                # Puedes añadir más campos del lugar si necesitas mostrarlos en tu frontend,
                # por ejemplo, para tarjetas de destino más ricas
                "regiones": item["lugar"]["regiones"],
                "climas_ideal": item["lugar"]["climas_ideal"],
                "accesibilidad_texto": item["lugar"]["accesibilidad_texto"],
                "presupuesto_requerido": item["lugar"]["preferencias_genericas"].get("Presupuesto", [])
            })

        print(f"Recomendaciones generadas: {recomendaciones_para_json}")
        
        return jsonify({
            "mensaje": "¡Aquí tienes algunas ciudades que podrían interesarte según tus preferencias!",
            "recomendaciones": recomendaciones_para_json
        }), 200 # Código de estado HTTP 200 OK
    else:
        print("No se encontraron recomendaciones para las preferencias recibidas.")

        # Si no se encontraron recomendaciones, devuelve un mensaje apropiado
        return jsonify({
            "mensaje": "Lo siento, no encontramos ningún lugar que coincida con tus preferencias. Intenta con otras opciones.",
            "recomendaciones": []
        }), 200 # Aunque no haya resultados, la operación fue exitosa

if __name__ == '__main__':
    app.run(debug=True)