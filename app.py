from flask import Flask, render_template
from database.db import get_connection

app = Flask(__name__)

@app.route("/")
def home():

    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS total FROM Status")
            result = cursor.fetchone()

        connection.close()

        return render_template(
        "index.html",
        total=result["total"]
    )

    except Exception as error:
        return f"""
        <h1>Kļūda</h1>
        <pre>{error}</pre>
        """

if __name__ == "__main__":
    app.run(debug=True)