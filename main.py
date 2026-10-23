import requests

RAPIDAPI_KEY = "21b1bfa893msha5edca65a085f4bp17cc86jsn412f7bba419e"
RAPIDAPI_HOST = "bet365data.p.rapidapi.com"

headers = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": RAPIDAPI_HOST
}

def rastrear_endpoint_correcto():
    print("Iniciando escaneo de rutas (Fuerza bruta)...\n")
    
    # Lista de las rutas más habituales para partidos futuros en RapidAPI
    rutas_posibles = [
        "/prematch-events/sports",
        "/upcoming",
        "/prematch",
        "/fixtures",
        "/v1/sports/upcoming",
        "/v2/bet365/upcoming",
        "/upcoming-events",
        "/v1/bet365/prematch"
    ]
    
    encontrado = False
    
    for ruta in rutas_posibles:
        url = f"https://{RAPIDAPI_HOST}{ruta}"
        try:
            res = requests.get(url, headers=headers)
            print(f"Probando: {ruta} -> Estado: {res.status_code}")
            
            if res.status_code == 200:
                print("\n✅ ¡ÉXITO! LA RUTA CORRECTA ES:")
                print(url)
                encontrado = True
                break
        except Exception as e:
            print(f"Fallo de conexión en {ruta}: {e}")
            
    if not encontrado:
        print("\n❌ Ninguna ruta estándar funcionó. Necesitamos revisar la documentación de RapidAPI.")

if __name__ == "__main__":
    rastrear_endpoint_correcto()
