from flask import Flask, request, jsonify, render_template_string
import json
import os

app = Flask(__name__)
DB_FILE = "global_database.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4, ensure_ascii=False)

# Главная страница (для друга в браузере)
@app.route('/')
def index():
    db = load_db()
    players = []
    for name, data in db.items():
        if name.lower() != "admin":
            players.append({"name": name, "elo": data['elo']})
    
    sorted_players = sorted(players, key=lambda x: x['elo'], reverse=True)
    
    html = """
    <body style="background:#111; color:white; font-family:sans-serif; text-align:center; padding-top:50px;">
        <h1 style="color:#00ffcc;">GLOBAL MATH ARENA TOP</h1>
        <table style="margin:auto; border-collapse:collapse; width:300px; background:#222; border-radius:10px;">
            <tr style="border-bottom:2px solid #555; background:#333; color:#00ffcc;">
                <th style="padding:10px;">RANK</th>
                <th style="padding:10px;">NAME</th>
                <th style="padding:10px;">ELO</th>
            </tr>
            {% for p in players %}
            <tr style="border-bottom:1px solid #444;">
                <td style="padding:8px;">{{ loop.index }}</td>
                <td style="padding:8px;">{{ p.name }}</td>
                <td style="padding:8px; font-weight:bold; color:#f1c40f;">{{ p.elo }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    """
    return render_template_string(html, players=sorted_players)

# Служебный путь (для игры)
@app.route('/sync', methods=['POST'])
def sync():
    data = request.json
    db = load_db()
    
    name = data['name']
    stats = data['stats']
    
    # Регистрация или Вход
    if name not in db:
        db[name] = stats
    else:
        # Если пароль верный — обновляем ELO и золото
        if db[name]['pass'] == stats['pass']:
            db[name]['elo'] = stats['elo']
            db[name]['gold'] = stats['gold']
            
    save_db(db)
    # Возвращаем обновленный топ всех игроков для меню в игре
    return jsonify({"status": "ok", "full_db": db})

if __name__ == "__main__":
    # Настройка для Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
