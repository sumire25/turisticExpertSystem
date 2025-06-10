from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- FRONTEND: rutas para mostrar páginas ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resultado', methods=['POST'])
def resultado():
    # Aquí puedes simular datos o dejarlo vacío por ahora
    intereses = request.form.get('intereses', '')
    lugares = []
    return render_template('resultado.html', intereses=intereses, lugares=lugares)

# --- BACKEND: API para lógica de recomendación ---
@app.route('/api/recomendar', methods=['POST'])
def recomendar():
    intereses = request.json.get('intereses', [])
    # Aquí irá la lógica real de recomendación
    lugares = []  # Por ahora, lista vacía
    return jsonify({'lugares': lugares})

if __name__ == '__main__':
    app.run(debug=True)