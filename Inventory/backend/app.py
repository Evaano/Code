from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

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

def get_inventory_data(category=None, subcategory=None):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    if category and subcategory:
        cursor.execute("SELECT * FROM inventory WHERE category = ? AND subcategory = ?", (category, subcategory))
    elif category:
        cursor.execute("SELECT * FROM inventory WHERE category = ?", (category,))
    elif subcategory:
        cursor.execute("SELECT * FROM inventory WHERE subcategory = ?", (subcategory,))
    else:
        cursor.execute("SELECT * FROM inventory")

    rows = cursor.fetchall()

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

inventory_data = get_inventory_data()

conn.close()

def add_item_to_database(
    item_code,
    item_description,
    category,
    subcategory,
    unit,
    brand,
    inwards,
    outwards,
    reorder,
):
    try:
        inwards = int(inwards)
        outwards = int(outwards)
    except ValueError:
        return jsonify({"error": "Invalid input for numeric fields. Item not added."}), 400

    current_stock = inwards - outwards
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    cursor.execute("SELECT item_code FROM inventory WHERE item_code=?", (item_code,))
    existing_item_code = cursor.fetchone()
    cursor.execute(
        "SELECT item_description FROM inventory WHERE item_description=?",
        (item_description,),
    )
    existing_item_description = cursor.fetchone()

    if existing_item_code or existing_item_description:
        return jsonify({"error": "Item already exists."}), 400

    cursor.execute(
        """
        INSERT INTO inventory
        (item_code, item_description, category, subcategory, unit, brand, inwards, outwards, current_stock, reorder)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            item_code,
            item_description,
            category,
            subcategory,
            unit,
            brand,
            inwards,
            outwards,
            current_stock,
            reorder,
        ),
    )
    conn.commit()
    conn.close()
    return jsonify({"message": f"Added item '{item_description}' to the inventory."})

def get_max_item_code():
    try:
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(item_code) FROM inventory")
        result = cursor.fetchone()
        max_item_code = result[0] if result and result[0] is not None else 0
        return int(max_item_code)
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return 0
    finally:
        if conn:
            conn.close()

@app.route('/api/maxItemCode', methods=['GET'])
def max_item_code():
    max_item_code = get_max_item_code()
    return jsonify({'maxItemCode': max_item_code})


@app.route('/api/inventory', methods=['GET'])
def get_inventory():
    category = request.args.get('category')
    subcategory = request.args.get('subcategory')
    inventory_data = get_inventory_data(category, subcategory)
    return jsonify({"inventory": inventory_data})

@app.route('/api/addItem', methods=['POST'])
def add_item():
    data = request.json
    
    result = add_item_to_database(
        data['item_code'],
        data['item_description'],
        data['category'],
        data['subcategory'],
        data['unit'],
        data['brand'],
        data['inwards'],
        data['outwards'],
        data['reorder'],
    )
    return result

if __name__ == '__main__':
    app.run(debug=True)