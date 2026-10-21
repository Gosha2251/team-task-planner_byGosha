import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="team_task_planner",
        cursorclass=pymysql.cursors.DictCursor
    )