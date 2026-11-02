import os
import sqlite3

from flask import Flask, g, jsonify, request, send_from_directory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")
DB_PATH = os.environ.get("DATABASE_PATH", os.path.join(BASE_DIR, "ecommerce.db"))

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def error(message, status):
    return jsonify({"error": message}), status


PRODUCT_SELECT = """
    SELECT p.id, p.name, p.description, p.price, p.image_url, p.stock,
           c.id AS category_id, c.name AS category
    FROM products p JOIN categories c ON c.id = p.category_id
"""


@app.get("/api/categories")
def list_categories():
    rows = get_db().execute("SELECT id, name FROM categories ORDER BY name").fetchall()
    return jsonify([dict(r) for r in rows])


@app.get("/api/products")
def list_products():
    """Optional query params: search, category (id), min_price, max_price."""
    search = request.args.get("search", "").strip()
    if len(search) > 100:
        return error("'search' must be at most 100 characters", 400)

    conditions, params = [], []
    if search:
        conditions.append("(p.name LIKE ? OR p.description LIKE ?)")
        params += [f"%{search}%", f"%{search}%"]

    category = request.args.get("category")
    if category:
        if not category.isdigit():
            return error("'category' must be a numeric id", 400)
        conditions.append("p.category_id = ?")
        params.append(int(category))

    for key, op in (("min_price", ">="), ("max_price", "<=")):
        value = request.args.get(key)
        if value:
            try:
                number = float(value)
            except ValueError:
                return error(f"'{key}' must be a number", 400)
            if number < 0:
                return error(f"'{key}' cannot be negative", 400)
            conditions.append(f"p.price {op} ?")
            params.append(number)

    query = PRODUCT_SELECT
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY p.id"

    rows = get_db().execute(query, params).fetchall()
    return jsonify([dict(r) for r in rows])


@app.get("/api/products/<product_id>")
def get_product(product_id):
    if not product_id.isdigit():
        return error("Product id must be a positive integer", 400)
    row = get_db().execute(PRODUCT_SELECT + " WHERE p.id = ?", (int(product_id),)).fetchone()
    if row is None:
        return error("Product not found", 404)
    return jsonify(dict(row))


@app.errorhandler(404)
def not_found(_e):
    if request.path.startswith("/api/"):
        return error("Resource not found", 404)
    return "Page not found", 404


@app.get("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        raise SystemExit("Database not found. Run:  python backend/init_db.py")
    app.run(host="127.0.0.1", port=5000, debug=True)