import os
import request

Steam64ID = os.getenv("MY_STEAM_64ID")
SteamAPI = os.getenv("MY_STEAM_API")

def get_Steam_data():
   url = f"http://steampowered.com{STEAM_API_KEY}&steamid={STEAM_ID}&format=json"
  try:
    response = requests.get(url).json()
    if "games" in response.get("response", {}):
      game = response["response"]["games"][0] 
      game_name = game["name"]
      playtime_2weeks = round(game["playtime_2weeks"] / 60, 1) 
      
      return f"""
<div align="center">
  <span>🎮 <b>Сейчас играет или недавно играл в:</b> {game_name} ({playtime_2weeks} ч. за последние 2 недели)</span>
</div>
"""
  except Exception as e:
    print(f"Ошибка при запросе к Steam API: {e}")

  return "<div align='center'>💤 не в сети</div>"
