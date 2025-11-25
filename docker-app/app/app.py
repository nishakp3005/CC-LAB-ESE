import os
from flask import Flask, jsonify
from sqlalchemy import create_engine, text

app = Flask(__name__)

# Default to local PostgreSQL if not in Docker environment
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://myuser:mypassword@localhost:5432/myapp")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=False, future=True)

# On startup, create a simple table if not exists
with engine.begin() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS visits (
            id SERIAL PRIMARY KEY,
            message TEXT
        )
    """))

@app.route("/")
def index():
    # Insert a row and count rows
    with engine.begin() as conn:
        conn.execute(text("INSERT INTO visits (message) VALUES (:msg)"),
                     {"msg": "Hello from Docker + Postgres!"})
        result = conn.execute(text("SELECT COUNT(*) FROM visits"))
        (count,) = result.fetchone()

    return jsonify({
        "message": "Hello, Nishita! Your Dockerized app is working.",
        "total_visits": int(count)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
