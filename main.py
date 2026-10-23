import requests

# 1. TUS CLAVES Y CHAT ID
RAPIDAPI_KEY = "21b1bfa893msha5edca65a085f4bp17cc86jsn412f7bba419e"
RAPIDAPI_HOST = "bet365data.p.rapidapi.com"
TELEGRAM_TOKEN = "8888052898:AAEYS2_2bsyxd0p1GXBrcrpQe6XYh0xEg1M"
TELEGRAM_CHAT_ID = "1203879706"

headers = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": RAPIDAPI_HOST
}

def enviar_alerta(mensaje):
    """Envía la alerta directamente a tu bot de Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje,
        "parse_mode": "Markdown"
    }
    try:
        res = requests.post(url, json=payload)
        res.raise_for_status()
        print("Mensaje enviado correctamente a Telegram.")
    except Exception as e:
        print(f"Error enviando mensaje a Telegram: {e}")

def comprobar_cuotas_bet365():
    # Probamos endpoints comunes de eventos en directo y programados
    endpoints = [
        f"https://{RAPIDAPI_HOST}/upcoming-events/sports",
        f"https://{RAPIDAPI_HOST}/live-events/sports"
    ]
    
    for url in endpoints:
        try:
            response = requests.get(url, headers=headers)
            print(f"Probando {url.split('/')[-1]} - HTTP Status: {response.status_code}")
            
            if response.status_code == 200:
                datos = response.json()
                
                # Extraer lista de eventos independientemente del formato del JSON
                if isinstance(datos, list):
                    eventos = datos
                elif isinstance(datos, dict):
                    eventos = datos.get("results", datos.get("data", datos.get("events", [])))
                else:
                    eventos = []
                    
                print(f"Eventos encontrados: {len(eventos)}")
                
                for evento in eventos:
                    home = evento.get('home', {}).get('name', 'Local') if isinstance(evento.get('home'), dict) else 'Local'
                    away = evento.get('away', {}).get('name', 'Visitante') if isinstance(evento.get('away'), dict) else 'Visitante'
                    partido = f"{home} vs {away}"
                    
                    for mercado in evento.get("markets", []):
                        nombre_mercado = mercado.get("name", "Mercado")
                        
                        for seleccion in mercado.get("outcomes", []):
                            opcion = seleccion.get("name", "Opción")
                            try:
                                cuota = float(seleccion.get("odds", 0))
                            except (ValueError, TypeError):
                                cuota = 0.0
                            
                            # Filtro de cuota (puedes ajustarlo luego a 2.10)
                            if cuota >= 1.01:
                                prob_implicita = round((1 / cuota) * 100, 1)
                                mensaje = (
                                    f"🚨 *¡OPORTUNIDAD (+EV) EN BET365!*\n\n"
                                    f"⚽ *Partido:* {partido}\n"
                                    f"🎯 *Mercado:* {nombre_mercado} - `{opcion}`\n"
                                    f"💰 *Cuota Bet365:* `{cuota}`\n"
                                    f"📊 *Prob. Implícita:* {prob_implicita}%\n\n"
                                    f"📲 _Revisa las alineaciones y entra a la cuota._"
                                )
                                enviar_alerta(mensaje)
        except Exception as e:
            print(f"Error procesando {url}: {e}")

if __name__ == "__main__":
    comprobar_cuotas_bet365()
