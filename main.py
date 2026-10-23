import requests

# Clave de RapidAPI
RAPIDAPI_KEY = "21b1bfa893msha5edca65a085f4bp17cc86jsn412f7bba419e"

# REEMPLAZA CON TUS DATOS REALES DE TELEGRAM:
TELEGRAM_TOKEN = 8888052898:AAEYS2_2bsyxd0p1GXBrcrpQe6XYh0xEg1M
TELEGRAM_CHAT_ID = 1203879706

headers = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "bet365-data.p.rapidapi.com"
}

def enviar_alerta(mensaje):
    """Envía la alerta a Telegram."""
    if TELEGRAM_TOKEN == "PEGA_AQUI_TU_TOKEN_DE_BOTFATHER":
        print("Aviso: Debes configurar tu TELEGRAM_TOKEN en main.py")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje,
        "parse_mode": "Markdown"
    }
    try:
        res = requests.post(url, json=payload)
        res.raise_for_status()
    except Exception as e:
        print(f"Error al enviar mensaje a Telegram: {e}")

def comprobar_cuotas_bet365():
    """Consulta la API de Bet365 sin romper el script en caso de variaciones de formato."""
    url = "https://bet365-data.p.rapidapi.com/v1/bet365/events"
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Respuesta de la API - Estado HTTP: {response.status_code}")
        
        if response.status_code == 200:
            datos = response.json()
            eventos = datos.get("results", [])
            print(f"Eventos encontrados: {len(eventos)}")
            
            for evento in eventos:
                home = evento.get('home', {}).get('name', 'Equipo Local') if isinstance(evento.get('home'), dict) else 'Equipo Local'
                away = evento.get('away', {}).get('name', 'Equipo Visitante') if isinstance(evento.get('away'), dict) else 'Equipo Visitante'
                partido = f"{home} vs {away}"
                
                for mercado in evento.get("markets", []):
                    nombre_mercado = mercado.get("name", "Mercado")
                    
                    for seleccion in mercado.get("outcomes", []):
                        opcion = seleccion.get("name", "Opción")
                        try:
                            cuota = float(seleccion.get("odds", 0))
                        except (ValueError, TypeError):
                            cuota = 0.0
                        
                        # Filtro de cuota mayor o igual a 2.10
                        if cuota >= 2.10:
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
            print(f"Error en RapidAPI ({response.status_code}): {response.text}")

    except Exception as e:
        print(f"Error general durante la ejecución: {e}")

if __name__ == "__main__":
    comprobar_cuotas_bet365()
