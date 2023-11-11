from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

conn = sqlite3.connect("inventory.db")
conn.execute("PRAGMA case_sensitive_like = OFF")  # Ensure case-insensitive behavior
conn.execute(
    """
    CREATE TABLE IF NOT EXISTS inventory (
        item_code TEXT PRIMARY KEY,
        item_description TEXT COLLATE NOCASE,
        category TEXT COLLATE NOCASE,
        subcategory TEXT COLLATE NOCASE,
        unit TEXT COLLATE NOCASE,
        brand TEXT COLLATE NOCASE,
        inwards INTEGER,
        outwards INTEGER,
        current_stock INTEGER,
        reorder INTEGER
    )
    """
)
conn.commit()

def get_inventory_data(category=None):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    if category:
        cursor.execute("SELECT * FROM inventory WHERE category = ?", (category,))
    else:
        cursor.execute("SELECT * FROM inventory")
    rows = cursor.fetchall()

    # Convert rows into a list of dictionaries
    inventory_data = [
        {
            "item_code": row[0],
            "item_description": row[1],
            "category": row[2],
            "subcategory": row[3],
            "unit": row[4],
            "brand": row[5],
            "inwards": row[6],
            "outwards": row[7],
            "current_stock": row[8],
            "reorder": row[9],
        }
        for row in rows
    ]

    cursor.close()
    conn.close()
    return inventory_data

# Replace the mock data with actual data from the database
inventory_data = get_inventory_data()

conn.close()

@app.route('/api/inventory', methods=['GET'])
def get_inventory():
    category = request.args.get('category')
    inventory_data = get_inventory_data(category)
    return jsonify({"inventory": inventory_data})

if __name__ == '__main__':
    app.run(debug=True)