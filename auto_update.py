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

def update_readme(status_html):
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()
   
    start_marker = "<!-- STEAM_STATUS:START -->"
    end_marker = "<!-- STEAM_STATUS:END -->"
    
    start_pos = readme.find(start_marker)
    end_pos = readme.find(end_marker)
    
    # Если маркеры успешно найдены в файле README.md
    if start_pos != -1 and end_pos != -1:
        new_readme = (
            readme[:start_pos + len(start_marker)] 
            + "\n" + status_html + "\n" + 
            readme[end_pos:]
        )
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(new_readme)
    else:
        print("Ошибка: Маркеры не найдены в README.md! Проверьте разметку.")
if __name__ == "__main__":
    if STEAM_API_KEY and STEAM_ID:
        current_status = get_steam_data()
        update_readme(current_status)
    else:
        print("Ошибка: Переменные окружения STEAM_API_KEY или STEAM_ID не найдены.")
