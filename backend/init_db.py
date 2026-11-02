import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get("DATABASE_PATH", os.path.join(BASE_DIR, "ecommerce.db"))


def main():
    conn = sqlite3.connect(DB_PATH)
    for script in ("schema.sql", "seed.sql"):
        with open(os.path.join(BASE_DIR, "db", script), encoding="utf-8") as f:
            conn.executescript(f.read())
    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    conn.close()
    print(f"Database created at {DB_PATH} with {count} products.")


if __name__ == "__main__":
    main()