from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DATABASE = "database.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        sample_data = [
            ("SKU-8921", "Organic Almond Milk 1L", "Dairy", 250, 0),
            ("SKU-8922", "Oat Milk Barista Edition", "Dairy", 220, 3),
            ("SKU-4410", "Arabica Coffee 500g", "Beverages", 450, 7),
            ("SKU-2298", "Eco Laundry Detergent", "Household", 350, 2),
            ("SKU-2299", "Bamboo Paper Towels 12pk", "Household", 280, 5)
        ]
        cursor.executemany(
            "INSERT INTO products (sku, name, category, price, quantity) VALUES (?, ?, ?, ?, ?)",
            sample_data
        )

    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return jsonify({"message": "Smart Stock Inventory API Running"})

@app.route("/api/products", methods=["GET"])
def get_products():
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return jsonify([dict(row) for row in products])

@app.route("/api/dashboard", methods=["GET"])
def dashboard():
    conn = get_db_connection()

    total_products = conn.execute(
        "SELECT COUNT(*) FROM products"
    ).fetchone()[0]

    active_alerts = conn.execute(
        "SELECT COUNT(*) FROM products WHERE quantity <= 5"
    ).fetchone()[0]

    conn.close()

    return jsonify({
        "totalProducts": total_products,
        "totalSales": 6998560,
        "activeAlerts": active_alerts,
        "revenue": 3500940
    })

@app.route("/api/alerts", methods=["GET"])
def get_alerts():
    conn = get_db_connection()
    alerts = conn.execute("""
        SELECT sku, name AS product, category, quantity
        FROM products
        WHERE quantity <= 5
    """).fetchall()
    conn.close()

    result = []
    for row in alerts:
        qty = row["quantity"]
        status = "out-of-stock" if qty == 0 else \
                 "critical" if qty <= 2 else "low-stock"

        result.append({
            "sku": row["sku"],
            "product": row["product"],
            "category": row["category"],
            "qty": qty,
            "status": status
        })
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
