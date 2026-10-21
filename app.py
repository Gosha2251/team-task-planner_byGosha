from flask import Flask, render_template
from database.db import get_connection

app = Flask(__name__)

@app.route("/")
def home():

    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS total FROM Status")
        result = cursor.fetchone()

    connection.close()

    return render_template(
        "index.html",
        total=result["total"]
    )

@app.route("/tasks")
def tasks():

    connection = get_connection()

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                t.title,
                s.name AS status
            FROM Tasks t
            JOIN Status s
                ON t.status_id = s.id
        """)

        tasks = cursor.fetchall()

    connection.close()

    return render_template(
        "tasks.html",
        tasks=tasks
    )

@app.route("/team")
def team():
    return render_template("team.html")

if __name__ == "__main__":
    app.run(debug=True)