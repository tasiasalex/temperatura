import requests
import json
from datetime import datetime

def obtenir_dades_meteo():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 41.3888,
        "longitude": 2.159,
        "hourly": "temperature_2m",
        "timezone": "Europe/Berlin",
        "forecast_days": 1
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Obtenim la llista de temperatures de les 24 hores d'avui
        temperatures = data["hourly"]["temperature_2m"]
        return temperatures
    except Exception as e:
        print(f"Error en obtenir les dades: {e}")
        return None

def calcular_estadistiques(temps):
    if not temps:
        return None
    
    t_max = max(temps)
    t_min = min(temps)
    t_mitjana = sum(temps) / len(temps)
    
    return {
        "maxima": round(t_max, 2),
        "minima": round(t_min, 2),
        "mitjana": round(t_mitjana, 2),
        "unitat": "°C"
    }

def exportar_a_json(dades):
    # Generem el nom del fitxer amb la data actual: temp_YYYYMMDD.json
    data_actual = datetime.now().strftime("%Y%m%d")
    nom_fitxer = f"temp_{data_actual}.json"
    
    with open(nom_fitxer, 'w', encoding='utf-8') as f:
        json.dump(dades, f, ensure_ascii=False, indent=4)
    
    print(f"Fitxer generat correctament: {nom_fitxer}")

def main():
    print("Iniciant la recollida de dades meteorològiques...")
    llista_temps = obtenir_dades_meteo()
    
    if llista_temps:
        resultats = calcular_estadistiques(llista_temps)
        exportar_a_json(resultats)
    else:
        print("No s'han pogut processar les dades.")

if __name__ == "__main__":
    main()
