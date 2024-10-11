from flask import Flask
import redis
import os
import mysql.connector

app = Flask(__name__)

r = redis.Redis(host="redis", port=6379)

def get_db_connection():
    conn = mysql.connector.connect(
        host="mysql",
        user="root",
        password=os.environ.get('MYSQL_ROOT_PASSWORD'),
        database=os.environ.get('MYSQL_DATABASE')
    )
    return conn

@app.route("/")
def home():
    count = r.incr("hits")


    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO visits (count) VALUES (%s)", (count,))
    conn.commit()
    cursor.close()
    conn.close()

    return f"This page has been visited {count} times."

if __name__ == "__main__":
    app.run(host="0.0.0.0")











# from flask import Flask
# import redis

# app = Flask(__name__)

# r = redis.Redis(host="redis", port=6379)


# @app.route("/")
# def home():
#     count = r.incr("hits")
#     return f"This page has been visited {count} times."


# if __name__ == "__main__":
#     app.run(host="0.0.0.0")
