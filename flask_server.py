from flask import Flask, render_template, request
import json
import os
from datetime import datetime

app = Flask(__name__)

json_file = r"C:\Users\solim\Documents\AI_Machine_Learning\logins_dedector\logins.json"

# controllo se il file ce
if not os.path.exists(json_file):
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump([], f, indent=4)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/check", methods=["GET", "POST"])
def check():
    result = None
    message = None

    if request.method == "POST":
        name = request.form.get("user")
        pc = request.form.get("pc")
        date = request.form.get("date")
        activity = request.form.get("activity")

        # convertire in giorno e ora
        try:
            date_obj = datetime.fromisoformat(date)
            day = date_obj.weekday()
            hour = date_obj.hour
        except:
            message = "Formato data non valido"
            return render_template("check.html", result=result, message=message)

        # controllo se e sicuro o no
        result = "Normal" if activity == "login_success" else "Suspicious"

        # leggere i dati attuali
        with open(json_file, "r", encoding="utf-8") as f:
            logins = json.load(f)

        new_login = {
            "name": name,
            "pc": pc,
            "date": date,
            "day": day,
            "hour": hour,
            "activity": activity,
            "result": result
        }

        logins.append(new_login)

        # salvare i dati
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(logins, f, indent=4, ensure_ascii=False)

        message = "Login aggiunto correttamente!"

    return render_template("check.html", result=result, message=message)

@app.route("/dashboard")
def dashboard():
    filter_val = request.args.get("filter", "all")

    # leggere dati
    with open(json_file, "r", encoding="utf-8") as f:
        logs = json.load(f)

    # filtro
    if filter_val != "all":
        logs = [log for log in logs if log["result"] == filter_val]

    # ordinare in base alla data
    logs.sort(key=lambda x: x["date"], reverse=True)

    return render_template("dashboard.html", logs=logs, filter_val=filter_val)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)