from flask import Flask
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

        return f"""
        <h1>Virtuāls uzdevumu plānotājs komandai</h1>

        <p>Diplomdarba projekts</p>

        <hr>

        <h3>MariaDB tests</h3>

        <p>Datubāzes savienojums veiksmīgs ✅</p>

        <p>Statusu skaits datubāzē: {result['total']}</p>
        """

    except Exception as error:
        return f"""
        <h1>Kļūda</h1>
        <pre>{error}</pre>
        """

if __name__ == "__main__":
    app.run(debug=True)