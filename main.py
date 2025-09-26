from flask import Flask, render_template, jsonify
from datetime import date, datetime, timedelta
import calendar

app = Flask(__name__)

# ------------------------
# Lista de feriados (YYYY-MM-DD)
# ------------------------
HOLIDAYS = [
    "2025-10-12",  # Nossa Senhora Aparecida
    "2025-10-13",  # Dias dos professores
    "2025-11-02",  # Finados
    "2025-11-15",  # Proclamação da República
    "2025-11-20",  # Conciencia negra
    "2025-11-21",  # Conciencia negra
    "2025-12-08",  # Conciencia negra
]

def parse_holidays(holidays_list):
    return {datetime.strptime(s, "%Y-%m-%d").date() for s in holidays_list}

def is_school_day(d: date, holidays:set):
    return d.weekday() < 5 and d not in holidays

def count_school_days(start_date: date, end_date: date, holidays:set):
    current = start_date
    count = 0
    while current <= end_date:
        if is_school_day(current, holidays):
            count += 1
        current += timedelta(days=1)
    return count

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/dias")
def api_dias():
    today = date.today()
    target = date(2025, 12, 18)
    holidays = parse_holidays(HOLIDAYS)

    days_left = count_school_days(today, target, holidays) if today <= target else 0
    holidays_in_range = sorted([d.isoformat() for d in holidays if today <= d <= target])

    return jsonify({
        "today": today.isoformat(),
        "target": target.isoformat(),
        "days_left": days_left,
        "holidays": holidays_in_range,
        "finished": today > target
    })

@app.route("/api/meses")
def api_meses():
    today = date.today()
    target = date(2025, 12, 18)
    holidays = parse_holidays(HOLIDAYS)

    meses = {}
    current = today
    while current <= target:
        if is_school_day(current, holidays):
            key = f"{current.month:02d}/{current.year}"
            meses[key] = meses.get(key, 0) + 1
        current += timedelta(days=1)

    # Corrigir: só contar a partir de 'today', não o mês inteiro
    meses_ordenados = dict(sorted(meses.items(), key=lambda x: datetime.strptime(x[0], "%m/%Y")))
    return jsonify(meses_ordenados)

if __name__ == "__main__":
    app.run(debug=True)
