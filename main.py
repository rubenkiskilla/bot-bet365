import requests

# 1. TUS CLAVES (Tomadas de tu captura de RapidAPI)
RAPIDAPI_KEY = "21b1bfa893msha5edca65a085f4bp17cc86jsn412f7bba419e"
RAPIDAPI_HOST = "bet365data.p.rapidapi.com"

# 2. TUS DATOS DE TELEGRAM (Integrados)
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
    # URL exacta obtenida de cURL en RapidAPI
    url = f"https://{RAPIDAPI_HOST}/live-events/sports"
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Respuesta API HTTP Status: {response.status_code}")
        
        if response.status_code == 200:
            datos = response.json()
            eventos = datos if isinstance(datos, list) else datos.get("results", datos.get("data", datos.get("events", [])))
            print(f"Partidos/eventos analizados: {len(eventos)}")
            
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
                        
                        # Filtro de prueba (cuotas >= 1.01) para forzar el primer envío
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
        else:
            print(f"Error en la API Bet365 ({response.status_code}): {response.text}")

    except Exception as e:
        print(f"Error durante el escaneo: {e}")

if __name__ == "__main__":
    comprobar_cuotas_bet365()
