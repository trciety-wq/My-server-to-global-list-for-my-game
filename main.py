from flask import Flask, request, jsonify, render_template_string
import json, os

app = Flask(_name_)
DB_FILE = "database.json"

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return {}
    return {}

def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    db = load_db()
    players = []
    for name, data in db.items():
        if isinstance(data, dict) and 'elo' in data:
            players.append({"name": name, "elo": data['elo'], "class": data.get('class', 'Warrior')})
    
    sorted_p = sorted(players, key=lambda x: x['elo'], reverse=True)
    
    html = """
    <body style="background:#0f0f1f; color:#00ffcc; font-family:sans-serif; text-align:center;">
        <h1 style="text-shadow: 0 0 10px #00ffcc;">MATH ARENA: GLOBAL TOP</h1>
        <table style="margin:auto; border-collapse:collapse; background:#1a1a2e; border:2px solid #00ffcc; width:80%;">
            <tr style="background:#00ffcc; color:#1a1a2e;"><th>RANK</th><th>NAME</th><th>CLASS</th><th>ELO</th></tr>
            {% for p in players %}
            <tr style="border-bottom:1px solid #333;">
                <td>{{ loop.index }}</td><td>{{ p.name }}</td><td>{{ p.class }}</td><td style="color:#ffcc00;">{{ p.elo }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    """
    return render_template_string(html, players=sorted_p)

@app.route('/sync', methods=['POST'])
def sync():
    data = request.json
    db = load_db()
    name = data.get('name')
    if name:
        db[name] = data.get('stats')
        save_db(db)
    return jsonify({"status": "ok", "full_db": db})

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
