import os
import requests

STEAM_API_KEY = os.getenv("STEAM_API_KEY")
STEAM_ID = os.getenv("STEAM_ID")

def get_steam_profile_and_game():
    profile_url = f"http://steampowered.com{STEAM_API_KEY}&steamids={STEAM_ID}"
    game_url = f"http://steampowered.com{STEAM_API_KEY}&steamid={STEAM_ID}&format=json"
    
    username = "Vorbanux"
    avatar_url = "https://github.com"
    status_text = "offline"
    status_color = "#8b929a"
    game_info_html = "Сейчас не в сети или играет во что-то секретное 🤫"

    try:
        profile_res = requests.get(profile_url).json()
        players = profile_res.get("response", {}).get("players", [])
        if players:
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
            else:
                status_text = "не в сети"
                status_color = "#8b929a"

        game_res = requests.get(game_url).json()
        if "games" in game_res.get("response", {}):
            game = game_res["response"]["games"][0]
            game_name = game["name"]
            playtime_2weeks = round(game["playtime_2weeks"] / 60, 1)
            game_info_html = f"🕹️ <b>{game_name}</b> ({playtime_2weeks} ч. за 2 недели)"

    except Exception as e:
        print(f"Ошибка API: {e}")

    html = '<table border="0" cellpadding="0" cellspacing="0" width="100%"><tr>'
    html += f'<td width="120" valign="top"><img src="{avatar_url}" width="100" height="100" style="border: 2px solid {status_color}; border-radius: 4px;" /></td>'
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
