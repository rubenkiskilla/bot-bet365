import requests
import time

RAPIDAPI_KEY = "21b1bfa893msha5edca65a085f4bp17cc86jsn412f7bba419e"
RAPIDAPI_HOST = "bet365data.p.rapidapi.com"
TELEGRAM_TOKEN = "8888052898:AAEYS2_2bsyxd0p1GXBrcrpQe6XYh0xEg1M"
TELEGRAM_CHAT_ID = "1203879706"

headers = {"x-rapidapi-key": RAPIDAPI_KEY, "x-rapidapi-host": RAPIDAPI_HOST}

def escanear_en_vivo():
    # 1. Buscamos partidos en directo (ruta confirmada que da HTTP 200)
    url_live = f"https://{RAPIDAPI_HOST}/live-events/sports"
    
    try:
        res = requests.get(url_live, headers=headers)
        eventos = res.json() if res.status_code == 200 else []
        eventos = eventos if isinstance(eventos, list) else eventos.get("results", [])
        
        print(f"Partidos en vivo ahora mismo: {len(eventos)}")
        
        # 2. Entramos a cada partido con la ruta de tu captura
        for ev in eventos:
            fi = ev.get("fi") or ev.get("id")
            if not fi: continue
            
            # Ruta exacta de "Get Event Markets"
            url_mercados = f"https://{RAPIDAPI_HOST}/events/{fi}"
            res_mercados = requests.get(url_mercados, headers=headers)
            
            if res_mercados.status_code == 200:
                # Aquí iría el filtro de cuotas (ej. cuota >= 2.10)
                print(f"Mercados obtenidos para el ID {fi}")
                
            time.sleep(1) # Pausa para evitar bloqueos
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    escanear_en_vivo()
