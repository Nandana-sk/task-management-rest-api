
import os
import sqlite3

from flask import Flask, jsonify, request, g


def init_db(database_path):
    """Create the database table if it does not exist."""
    connection = sqlite3.connect(database_path)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()


def create_app(database_path=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)

    app.config["DATABASE"] = database_path or os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "tasks.db"
    )

    init_db(app.config["DATABASE"])

    def get_db():
        """Get a database connection for the current request."""
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DATABASE"])
            g.db.row_factory = sqlite3.Row

        return g.db

    @app.teardown_appcontext
    def close_db(exception=None):
        """Close the database connection after a request."""
        db = g.pop("db", None)

        if db is not None:
            db.close()

    def format_task(row):
        """Convert a database row into a JSON-friendly dictionary."""
        return {
            "id": row["id"],
            "title": row["title"],
            "completed": bool(row["completed"])
        }

    @app.route("/tasks", methods=["GET"])
    def get_tasks():
        db = get_db()

        rows = db.execute(
            "SELECT id, title, completed FROM tasks ORDER BY id"
        ).fetchall()

        return jsonify({"tasks": [format_task(row) for row in rows]})

    @app.route("/tasks", methods=["POST"])
    def create_task():
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "error": "Request body must be a JSON object"
            }), 400

        title = data.get("title")

        if not isinstance(title, str) or not title.strip():
            return jsonify({"error": "Title is required"}), 400

        db = get_db()

        cursor = db.execute(
            "INSERT INTO tasks (title, completed) VALUES (?, ?)",
            (title.strip(), 0)
        )

        db.commit()

        row = db.execute(
            "SELECT id, title, completed FROM tasks WHERE id = ?",
            (cursor.lastrowid,)
        ).fetchone()

        return jsonify(format_task(row)), 201

    @app.route("/tasks/<int:task_id>", methods=["PUT"])
    def update_task(task_id):
        data = request.get_json(silent=True)

        if not isinstance(data, dict) or not data:
            return jsonify({
                "error": "Request body must be a non-empty JSON object"
            }), 400

        allowed_fields = {"title", "completed"}

        if not set(data).issubset(allowed_fields):
            return jsonify({"error": "Unknown field"}), 400

        db = get_db()

        row = db.execute(
            "SELECT id, title, completed FROM tasks WHERE id = ?",
            (task_id,)
        ).fetchone()

        if row is None:
            return jsonify({"error": "Task not found"}), 404

        title = row["title"]
        completed = bool(row["completed"])

        if "title" in data:
            if not isinstance(data["title"], str) or not data["title"].strip():
                return jsonify({"error": "Title is required"}), 400

            title = data["title"].strip()

        if "completed" in data:
            if not isinstance(data["completed"], bool):
                return jsonify({
                    "error": "Completed must be true or false"
                }), 400

            completed = data["completed"]

        db.execute(
            "UPDATE tasks SET title = ?, completed = ? WHERE id = ?",
            (title, int(completed), task_id)
        )

        db.commit()

        updated_row = db.execute(
            "SELECT id, title, completed FROM tasks WHERE id = ?",
            (task_id,)
        ).fetchone()

        return jsonify(format_task(updated_row)), 200

    @app.route("/tasks/<int:task_id>", methods=["DELETE"])
    def delete_task(task_id):
        db = get_db()

        cursor = db.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )

        if cursor.rowcount == 0:
            return jsonify({"error": "Task not found"}), 404

        db.commit()

        return "", 204

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
