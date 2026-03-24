from flask import Flask, request, jsonify, render_template_string
import json, os

app = Flask(__name__)
DB_FILE = "database.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    db = load_db()
    players = []
    # Проверяем, что данные — это словарь
    if isinstance(db, dict):
        for name, data in db.items():
            if isinstance(data, dict) and 'elo' in data:
                players.append({"name": name, "elo": data['elo']})
    
    sorted_p = sorted(players, key=lambda x: x['elo'], reverse=True)
    
    html = """
    <body style="background:#0a0a1a; color:#00ffcc; font-family:sans-serif; text-align:center; padding-top:50px;">
        <h1 style="text-shadow: 0 0 10px #00ffcc;">GLOBAL MATH ARENA TOP</h1>
        <table style="margin:auto; border-collapse:collapse; background:#161625; border:2px solid #00ffcc; width:80%; max-width:500px;">
            <tr style="background:#00ffcc; color:#0a0a1a;">
                <th style="padding:10px;">RANK</th><th style="padding:10px;">NAME</th><th style="padding:10px;">ELO</th>
            </tr>
            {% for p in players %}
            <tr style="border-bottom:1px solid #333;">
                <td style="padding:10px;">{{ loop.index }}</td>
                <td style="padding:10px;">{{ p.name }}</td>
                <td style="padding:10px; color:#ffcc00; font-weight:bold;">{{ p.elo }}</td>
            </tr>
            {% endfor %}
        </table>
        {% if not players %}<p style="margin-top:20px;">Арена пуста. Будь первым!</p>{% endif %}
    </body>
    """
    return render_template_string(html, players=sorted_p)

@app.route('/sync', methods=['POST'])
def sync():
    try:
        data = request.json
        if not data: return jsonify({"error": "No data"}), 400
        
        db = load_db()
        name = data.get('name')
        stats = data.get('stats')
        
        if name and stats:
            db[name] = stats
            save_db(db)
            
        return jsonify({"status": "ok", "full_db": db})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
