import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def buscar_numeros():
    # 1. La fuente de datos (Usamos una de las más estables en RD)
    url = "https://www.conectate.com.do/loterias/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        print("Buscando números en tiempo real...")
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        datos_finales = {
            "actualizado": datetime.now().strftime("%d/%m/%Y %I:%M %p"),
            "loterias": []
        }

        # 2. Localizar los contenedores de los sorteos
        # En esta web, cada sorteo está en un div con una clase específica
        sorteos = soup.find_all('div', class_='lottery-res-list')

        for sorteo in sorteos:
            try:
                # Extraer nombre (Ej: Gana Más, Quiniela Pale)
                nombre = sorteo.find('h3').get_text(strip=True)
                
                # Extraer los bolos/números
                bolos = sorteo.find_all('span', class_='ball')
                numeros = [bolo.get_text(strip=True) for bolo in bolos]

                # Solo agregamos si tiene números (para evitar sorteos vacíos)
                if numeros:
                    datos_finales["loterias"].append({
                        "nombre": nombre,
                        "numeros": numeros[:3] # Tomamos los 3 premios principales
                    })
            except Exception as e:
                print(f"Error procesando un sorteo: {e}")
                continue

        # 3. Guardar los resultados en el archivo JSON
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(datos_finales, f, indent=4, ensure_ascii=False)
        
        print("¡Éxito! data.json ha sido actualizado.")

    except Exception as e:
        print(f"Error general en el scraper: {e}")
if _name_ == "_main_":
    buscar_numeros()
