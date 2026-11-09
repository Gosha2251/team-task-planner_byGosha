from flask import Flask, render_template, request, redirect
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
                t.id,
                t.title,
                t.description,
                s.name AS status
            FROM Tasks t
            JOIN Status s
                ON t.status_id = s.id
            ORDER BY t.id DESC
        """)

        tasks = cursor.fetchall()

    connection.close()

    return render_template(
        "tasks.html",
        tasks=tasks
    )

@app.route("/tasks/add", methods=["GET", "POST"])
def add_task():

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]

        connection = get_connection()

        with connection.cursor() as cursor:

            cursor.execute("""
                INSERT INTO Tasks
                (
                    title,
                    description,
                    status_id,
                    assigned_to,
                    team_id
                )
                VALUES
                (%s, %s, 1, 1, 1)
            """, (title, description))

        connection.commit()
        connection.close()

        return redirect("/tasks")

    return render_template("add_task.html")

@app.route("/tasks/<int:task_id>")
def task_details(task_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    t.id,
                    t.title,
                    t.description,
                    t.created_at,
                    s.name AS status,
                    u.name AS assigned_user,
                    tm.name AS team_name
                FROM Tasks t
                JOIN Status s ON t.status_id = s.id
                LEFT JOIN Users u ON t.assigned_to = u.id
                JOIN Teams tm ON t.team_id = tm.id
                WHERE t.id = %s
            """, (task_id,))

            task = cursor.fetchone()

    finally:
        connection.close()

    if task is None:
        return "Uzdevums nav atrasts.", 404

    return render_template(
        "task_details.html",
        task=task
    )

@app.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
def edit_task(task_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            # Saglabājam lietotāja veiktās izmaiņas
            if request.method == "POST":
                title = request.form["title"].strip()
                description = request.form["description"].strip()
                status_id = request.form["status_id"]
                assigned_to = request.form["assigned_to"]

                if not title:
                    return "Uzdevuma nosaukums nedrīkst būt tukšs.", 400

                cursor.execute("""
                    UPDATE Tasks
                    SET
                        title = %s,
                        description = %s,
                        status_id = %s,
                        assigned_to = %s
                    WHERE id = %s
                """, (
                    title,
                    description,
                    status_id,
                    assigned_to,
                    task_id
                ))

                connection.commit()

                return redirect(f"/tasks/{task_id}")

            # Iegūstam pašreizējos uzdevuma datus
            cursor.execute("""
                SELECT
                    id,
                    title,
                    description,
                    status_id,
                    assigned_to
                FROM Tasks
                WHERE id = %s
            """, (task_id,))

            task = cursor.fetchone()

            if task is None:
                return "Uzdevums nav atrasts.", 404

            # Iegūstam statusus dropdown izvēlnei
            cursor.execute("""
                SELECT id, name
                FROM Status
                ORDER BY id
            """)
            statuses = cursor.fetchall()

            # Iegūstam lietotājus dropdown izvēlnei
            cursor.execute("""
                SELECT id, name
                FROM Users
                ORDER BY name
            """)
            users = cursor.fetchall()

    finally:
        connection.close()

    return render_template(
        "edit_task.html",
        task=task,
        statuses=statuses,
        users=users
    )

@app.route("/team")
def team():
    return render_template("team.html")

if __name__ == "__main__":
    app.run(debug=True)