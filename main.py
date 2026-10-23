import requests

# Clave tomada de tu pantalla en RapidAPI
RAPIDAPI_KEY = "21b1bfa893msha5edca65a085f4bp17cc86jsn412f7bba419e"

# Reemplaza con los datos que te dio Telegram
TELEGRAM_TOKEN = 8888052898:AAEYS2_2bsyxd0p1GXBrcrpQe6XYh0xEg1M
TELEGRAM_CHAT_ID = 1203879706


🧠 Explanations and answers
Free AI → DeepSeek (https://t.me/deepseek_gidbot) & ChatGPT (https://t.me/chatgpt_gidbot)

🖼 Visualize your ideas
Make Image → NanoBanana (https://t.me/nanobanana_gidbot)

headers = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "bet365-data.p.rapidapi.com"
}

def enviar_alerta(mensaje):
    """Envía la alerta directamente a tu Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

def comprobar_cuotas_bet365():
    """Consulta la API de Bet365 y detecta cuotas con valor."""
    url = "https://bet365-data.p.rapidapi.com/v1/bet365/events"
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            datos = response.json()
            eventos = datos.get("results", [])
            
            for evento in eventos:
                partido = f"{evento.get('home', {}).get('name')} vs {evento.get('away', {}).get('name')}"
                
                for mercado in evento.get("markets", []):
                    nombre_mercado = mercado.get("name", "Mercado")
                    
                    for seleccion in mercado.get("outcomes", []):
                        opcion = seleccion.get("name", "Opción")
                        cuota = float(seleccion.get("odds", 0))
                        
                        # Filtro de valor: Cuotas desajustadas por encima de 2.10
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
            print(f"Error {response.status_code}: Suscríbete primero en RapidAPI o verifica los parámetros.")

    except Exception as e:
        print(f"Error en la ejecución: {e}")

if __name__ == "__main__":
    comprobar_cuotas_bet365()
