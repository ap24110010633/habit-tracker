from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "final-hackathon-key"

habits = []
reminders = []


def get_badges():
    badges = []
    if any(h["streak"] >= 1 for h in habits):
        badges.append("Starter 🥉")
    if any(h["streak"] >= 3 for h in habits):
        badges.append("Consistent 🥈")
    if any(h["streak"] >= 7 for h in habits):
        badges.append("Champion 🥇")
    if habits and all(h["done"] for h in habits):
        badges.append("Perfect Day 🎯")
    return badges


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["user"] = request.form["username"]
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        habits.append({
            "id": len(habits),
            "name": request.form["habit"],
            "done": False,
            "streak": 0
        })

    return render_template(
        "dashboard.html",
        habits=habits,
        badges=get_badges()
    )


@app.route("/done/<int:id>")
def done(id):
    for h in habits:
        if h["id"] == id and not h["done"]:
            h["done"] = True
            h["streak"] += 1
    return redirect(url_for("dashboard"))


@app.route("/today")
def today():
    return render_template("today.html", habits=habits)


@app.route("/streaks")
def streaks():
    return render_template("streaks.html", habits=habits)


@app.route("/analytics")
def analytics():
    return render_template("analytics.html", habits=habits)


@app.route("/reminders", methods=["GET", "POST"])
def reminders_page():
    if request.method == "POST":
        reminders.append({
            "date": request.form["date"],
            "tag": request.form["tag"],
            "note": request.form["note"]
        })
    return render_template("reminders.html", reminders=reminders)


@app.route("/settings")
def settings():
    return render_template("settings.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
