import os
import requests

STEAM_API_KEY = os.getenv("STEAM_API_KEY")
STEAM_ID = os.getenv("STEAM_ID")

def get_steam_profile_and_game():
    base_url = "https://steampowered.com"
    
    profile_path = "/ISteamUser/GetPlayerSummaries/v0002/"
    profile_url = f"{base_url}{profile_path}?key={STEAM_API_KEY}&steamids={STEAM_ID}"
    
    game_path = "/IPlayerService/GetRecentlyPlayedGames/v0001/"
    game_url = f"{base_url}{game_path}?key={STEAM_API_KEY}&steamid={STEAM_ID}&format=json"
    
    username = "Vorbanux"
    avatar_url = "steam_avatar.jpg"
    status_text = "offline"
    status_color = "#8b929a"
    game_info_html = "Не известно"

    try:
        # 1. ЗАПРОС ПРОФИЛЯ С ПРОВЕРКОЙ СТАТУСА
        profile_req = requests.get(profile_url)
        print(f"Статус ответа профиля Steam: {profile_req.status_code}")
        
        if profile_req.status_code == 200:
            try:
                profile_res = profile_req.json()
                players = profile_res.get("response", {}).get("players", [])
                if isinstance(players, list) and len(players) > 0:
                    player = players[0]
                    username = player.get("personaname", username)
                    avatar_url = player.get("avatarfull", avatar_url)
                    
                    state = player.get("personastate", 0)
                    if "gameextrainfo" in player:
                        status_text = "в игре"
                        status_color = "#90ba3c"
                    elif state > 0:
                        status_text = "в сети"
                        status_color = "#57cbde"
            except Exception as json_err:
                print(f"Не удалось распарсить JSON профиля: {json_err}")
                print(f"Сырой ответ сервера: {profile_req.text}")
        else:
            print(f"Steam вернул ошибку профиля. Код: {profile_req.status_code}. Проверьте ключи.")

        # 2. ЗАПРОС ИГРЫ С ПРОВЕРКОЙ СТАТУСА
        game_req = requests.get(game_url)
        print(f"Статус ответа игр Steam: {game_req.status_code}")
        
        if game_req.status_code == 200:
            try:
                game_res = game_req.json()
                games = game_res.get("response", {}).get("games", [])
                if isinstance(games, list) and len(games) > 0:
                    game = games[0]
                    game_name = game.get("name", "Игру")
                    playtime_2weeks = round(game.get("playtime_2weeks", 0) / 60, 1)
                    game_info_html = f"🕹️ <b>{game_name}</b> ({playtime_2weeks} ч. за 2 недели)"
            except Exception as json_err:
                print(f"Не удалось распарсить JSON игры: {json_err}")
        else:
            print(f"Steam вернул ошибку игр. Код: {game_req.status_code}")

    except Exception as e:
        print(f"Общая ошибка сети API: {e}")

    # Принудительно переводим аватарку на защищенный протокол https
    if avatar_url.startswith("http://"):
        avatar_url = avatar_url.replace("http://", "https://")

    # Безопасная сборка HTML
    html = '<table border="0" cellpadding="0" cellspacing="0" width="100%"><tr>'
    html += f'<td width="120" valign="top"><img src="{avatar_url}" width="100" height="100" style="border: 2px solid {status_color}; border-radius: 4px;" onerror="this.onerror=null;this.src=\'steam_avatar.jpg\';" /></td>'
    html += f'<td valign="top"><font size="5" color="#ffffff"><b>{username}</b></font>&nbsp;&nbsp;<font size="2" color="{status_color}">● {status_text}</font>'
    html += f'<br><br><font size="2" color="#8b929a">АКТИВНОСТЬ:</font><br><font size="3" color="#66c0f4">{game_info_html}</font></td>'
    html += '</tr></table>'
    return html

def update_readme(status_html):
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    start_marker = "<!-- STEAM_STATUS:START -->"
    end_marker = "<!-- STEAM_STATUS:END -->"
    
    start_pos = readme.find(start_marker)
    end_pos = readme.find(end_marker)
    
    if start_pos != -1 and end_pos != -1:
        new_readme = readme[:start_pos + len(start_marker)] + "\n" + status_html + "\n" + readme[end_pos:]
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(new_readme)
    else:
        print("Маркеры не найдены в README.md")

if __name__ == "__main__":
    if STEAM_API_KEY and STEAM_ID:
        status_html = get_steam_profile_and_game()
        update_readme(status_html)
    else:
        print("Критические переменные окружения пусты.")
