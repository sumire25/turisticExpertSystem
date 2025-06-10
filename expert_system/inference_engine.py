from .knowledge_base import lugares_turisticos_peru

def recomendar_lugares(memoria_de_trabajo_json):
    """
    Realiza la inferencia utilizando encadenamiento hacia adelante.
    Recibe preferencias del usuario como un diccionario (simulando JSON).

    Args:
        memoria_de_trabajo_json (dict): Diccionario con las preferencias del usuario.
                                   Ej: {
                                         "Clima": ["calido", "humedo"],
                                         "Aventura": ["kayak", "trekking"],
                                         "Presupuesto": "medio",
                                         "Transporte": "facil"
                                       }

    Returns:
        list: Lista de diccionarios, cada uno con el lugar recomendado (incluye descripción),
              puntuación y una lista de explicaciones.
    """
    # Normalizar las claves y valores de la memoria de trabajo a minúsculas
    # Se asegura que los valores de las listas también estén en minúsculas
    preferencias_usuario = {}
    for key, value in memoria_de_trabajo_json.items():
        if isinstance(value, list):
            preferencias_usuario[key.lower()] = [v.lower() for v in value]
        else:
            preferencias_usuario[key.lower()] = value.lower()
    
    resultados_con_puntuacion = []
    
    for lugar in lugares_turisticos_peru:
        puntuacion = 0
        explicaciones = []
        
        # --- Reglas de Producción (Encadenamiento Hacia Adelante) ---

        # 1. Regla: Coincidencia de Clima (Alto peso: 10)
        if "clima" in preferencias_usuario and preferencias_usuario["clima"]:
            for clima_pref in preferencias_usuario["clima"]:
                if clima_pref in [c.lower() for c in lugar["climas_ideal"]]:
                    puntuacion += 10
                    explicaciones.append(f"✓ Coincide con el clima '{clima_pref.capitalize()}' deseado.")

        # 2. Regla: Coincidencia por tipo de Aventura (Peso: 5 por cada coincidencia)
        if "aventura" in preferencias_usuario and preferencias_usuario["aventura"]:
            for pref_act in preferencias_usuario["aventura"]:
                if pref_act in [a.lower() for a in lugar["preferencias_genericas"].get("Aventura", [])]:
                    puntuacion += 5
                    explicaciones.append(f"✓ Interés en **Aventura** ('{pref_act.capitalize()}') coincide.")
        
        # 3. Regla: Coincidencia por tipo de Cultura (Peso: 5 por cada coincidencia)
        if "cultura" in preferencias_usuario and preferencias_usuario["cultura"]:
            for pref_cult in preferencias_usuario["cultura"]:
                if pref_cult in [c.lower() for c in lugar["preferencias_genericas"].get("Cultura", [])]:
                    puntuacion += 5
                    explicaciones.append(f"✓ Interés en **Cultura** ('{pref_cult.capitalize()}') coincide.")

        # 4. Regla: Coincidencia por tipo de Gastronomía (Peso: 5 por cada coincidencia)
        if "gastronomia" in preferencias_usuario and preferencias_usuario["gastronomia"]:
            for pref_gast in preferencias_usuario["gastronomia"]:
                if pref_gast in [g.lower() for g in lugar["preferencias_genericas"].get("Gastronomia", [])]:
                    puntuacion += 5
                    explicaciones.append(f"✓ Interés en **Gastronomía** ('{pref_gast.capitalize()}') coincide.")

        # 5. Regla: Coincidencia por tipo de Naturaleza (Peso: 5 por cada coincidencia)
        if "naturaleza" in preferencias_usuario and preferencias_usuario["naturaleza"]:
            for pref_nat in preferencias_usuario["naturaleza"]:
                if pref_nat in [n.lower() for n in lugar["preferencias_genericas"].get("Naturaleza", [])]:
                    puntuacion += 5
                    explicaciones.append(f"✓ Interés en **Naturaleza** ('{pref_nat.capitalize()}') coincide.")

        # 6. Regla: Coincidencia de Presupuesto (Peso: 3)
        if "presupuesto" in preferencias_usuario and "Presupuesto" in lugar["preferencias_genericas"]:
            if preferencias_usuario["presupuesto"] in [p.lower() for p in lugar["preferencias_genericas"]["Presupuesto"]]:
                puntuacion += 3
                explicaciones.append(f"✓ Adecuado para un presupuesto '{preferencias_usuario['presupuesto'].capitalize()}'.")
        
        # 7. Regla: Coincidencia de Tipo de Compañía (Peso: 2)
        if "tipo de compañia" in preferencias_usuario and "Tipo de Compañía" in lugar["preferencias_genericas"]:
            if preferencias_usuario["tipo de compañia"] in [tc.lower() for tc in lugar["preferencias_genericas"]["Tipo de Compañía"]]:
                puntuacion += 2
                explicaciones.append(f"✓ Ideal para viajar '{preferencias_usuario['tipo de compañia'].capitalize()}'.")

        # 8. Regla: Coincidencia de Duración del Viaje (Peso: 2)
        if "duracion del viaje" in preferencias_usuario and "Duración del Viaje" in lugar["preferencias_genericas"]:
            if preferencias_usuario["duracion del viaje"] in [dv.lower() for dv in lugar["preferencias_genericas"]["Duración del Viaje"]]:
                puntuacion += 2
                explicaciones.append(f"✓ Adecuado para una duración de viaje de '{preferencias_usuario['duracion del viaje'].capitalize()}'.")

        # 9. Regla: Coincidencia de Accesibilidad (Peso: 4)
        if "transporte" in preferencias_usuario: # "Transporte" es la clave en tu JSON de entrada
            pref_transporte = preferencias_usuario["transporte"]
            acc_lugar = lugar["accesibilidad_texto"].lower() # Usamos el campo accesibilidad_texto para comparar
            
            if pref_transporte == "alta" and acc_lugar == "alta":
                puntuacion += 4
                explicaciones.append("✓ Preferencia por accesibilidad 'Alta'.")
            elif pref_transporte == "media" and acc_lugar == "media":
                puntuacion += 3
                explicaciones.append("✓ Preferencia por accesibilidad 'Media'.")
            elif pref_transporte == "dificil" and (acc_lugar == "dificil" or acc_lugar == "muy dificil"):
                puntuacion += 4
                explicaciones.append("✓ Disposición a una accesibilidad 'Difícil'.")
            # Podrías añadir una opción 'no importa' si es relevante
            elif pref_transporte == "no importa":
                puntuacion += 1 # Puntuación leve si no hay restricción
                explicaciones.append("✓ No hay restricción de transporte (se adapta a la accesibilidad del lugar).")
        
        # --- Final de la inferencia para un lugar ---
        
        if puntuacion > 0:
            resultados_con_puntuacion.append({
                "lugar": lugar,
                "puntuacion": puntuacion,
                "explicaciones": explicaciones
            })

    # Resolución de Conflictos: Ordenar por puntuación (de mayor a menor)
    resultados_con_puntuacion.sort(key=lambda x: x["puntuacion"], reverse=True)

    # Devolver los top N resultados
    return resultados_con_puntuacion[:5] # Por ejemplo, los 5 mejores