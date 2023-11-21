from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})


def connect_to_database():
    return sqlite3.connect("inventory.db")


conn = connect_to_database()
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
    conn = connect_to_database()
    cursor = conn.cursor()
    if category and subcategory:
        cursor.execute(
            "SELECT * FROM inventory WHERE category = ? AND subcategory = ?",
            (category, subcategory),
        )
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
        return (
            jsonify({"error": "Invalid input for numeric fields. Item not added."}),
            400,
        )

    current_stock = inwards - outwards
    conn = connect_to_database()
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
        conn = connect_to_database()
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


@app.route("/api/maxItemCode", methods=["GET"])
def max_item_code():
    max_item_code = get_max_item_code()
    return jsonify({"maxItemCode": max_item_code})


@app.route("/api/inventory", methods=["GET"])
def get_inventory():
    category = request.args.get("category")
    subcategory = request.args.get("subcategory")
    inventory_data = get_inventory_data(category, subcategory)
    return jsonify({"inventory": inventory_data})


@app.route("/api/add-item", methods=["POST"])
def add_item():
    data = request.json

    result = add_item_to_database(
        data["item_code"],
        data["item_description"],
        data["category"],
        data["subcategory"],
        data["unit"],
        data["brand"],
        data["inwards"],
        data["outwards"],
        data["reorder"],
    )
    return result


@app.route("/get-item-descriptions", methods=["GET"])
def get_item_descriptions():
    conn = connect_to_database()
    cursor = conn.cursor()

    input_value = request.args.get(
        "input", ""
    )  # Get the input value from the query parameter
    cursor.execute(
        "SELECT item_description FROM inventory WHERE item_description LIKE ?",
        ("%" + input_value + "%",),
    )
    descriptions = [row[0] for row in cursor.fetchall()]

    conn.close()

    return jsonify(descriptions)


@app.route("/search-item", methods=["POST"])
def search_item():
    data = request.get_json()

    selected_option = data.get("selected_option", "")
    item_to_update = selected_option

    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM inventory WHERE item_code=? OR item_description=?",
        (item_to_update, item_to_update),
    )
    existing_item = cursor.fetchone()

    if existing_item:
        item = {
            "item_code": existing_item[0],
            "item_description": existing_item[1],
            "category": existing_item[2],
            "subcategory": existing_item[3],
            "unit": existing_item[4],
            "brand": existing_item[5],
            "inwards": existing_item[6],
            "outwards": existing_item[7],
            "current_stock": existing_item[8],
            "reorder": existing_item[9],
        }
    else:
        conn.close()
        return jsonify({"error": "Item not found"}), 404

    conn.close()

    return jsonify(item)


def update_item_in_database(
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
        return (
            jsonify({"error": "Invalid input for numeric fields. Item not updated."}),
            400,
        )

    current_stock = inwards - outwards
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE inventory
        SET item_description=?, category=?, subcategory=?, unit=?, brand=?, inwards=?, outwards=?, current_stock=?, reorder=?
        WHERE item_code=?
        """,
        (
            item_description,
            category,
            subcategory,
            unit,
            brand,
            inwards,
            outwards,
            current_stock,
            reorder,
            item_code,
        ),
    )
    conn.commit()
    conn.close()
    return jsonify({"message": f"Updated item '{item_description}' in the inventory."})


@app.route("/api/update-item", methods=["PUT"])
def update_item():
    data = request.json

    result = update_item_in_database(
        data["item_code"],
        data["item_description"],
        data["category"],
        data["subcategory"],
        data["unit"],
        data["brand"],
        data["inwards"],
        data["outwards"],
        data["reorder"],
    )
    return result


def delete_item_from_database(item_code):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM inventory WHERE item_code=?", (item_code,))
        existing_item_code = cursor.fetchone()

        if existing_item_code:
            cursor.execute("DELETE FROM inventory WHERE item_code=?", (item_code,))
            conn.commit()
            conn.close()
            return (
                jsonify(
                    {
                        "message": f"Deleted item with code '{item_code}' from the inventory."
                    }
                ),
                200,
            )
        else:
            conn.close()
            return jsonify({"error": "Item not found."}), 404
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return jsonify({"error": "Error deleting item"}), 500


@app.route("/api/delete-item", methods=["DELETE"])
def delete_item():
    data = request.json
    item_code = data.get("item_code")

    if not item_code:
        return jsonify({"error": "Item Code is required."}), 400

    return delete_item_from_database(item_code)


if __name__ == "__main__":
    app.run(debug=True)
