import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

# Create or connect to the SQLite database with case-insensitive collation
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
conn.close()


def show_inventory_app(start_frame, notebook):
    # This function will be called when the "Proceed to Inventory App" button is clicked.
    start_frame.pack_forget()  # Hide the starting page frame
    notebook.pack(fill="both", expand=True)  # Show the inventory app


# Create or connect to the SQLite database with case-insensitive collation
# (your database creation code goes here)


def create_start_page(root, notebook):
    # Create a frame for the starting page
    start_frame = ttk.Frame(root)
    start_frame.pack(fill="both", expand=True)

    # Load and resize the image
    original_image = Image.open("start_image.png")
    resized_image = original_image.resize((300, 300))  # Adjust the dimensions as needed
    image = ImageTk.PhotoImage(resized_image)
    image_label = tk.Label(start_frame, image=image)
    image_label.image = image  # Keep a reference to the image to prevent it from being garbage collected
    image_label.pack(pady=20)

    # Add introductory text
    intro_label = tk.Label(start_frame, text="Welcome to the Inventory Management App")
    intro_label.pack(pady=20)

    # Add a button to proceed to the inventory app
    proceed_button = tk.Button(
        start_frame,
        text="Proceed",
        command=lambda: show_inventory_app(start_frame, notebook),
    )
    proceed_button.pack()

    return start_frame


def refresh_inventory_tree(tree):
    # Clear the existing items in the Treeview
    for item in tree.get_children():
        tree.delete(item)

    # Connect to the database
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    # Retrieve all items from the database
    cursor.execute("SELECT * FROM inventory")
    items = cursor.fetchall()

    # Close the connection
    conn.close()

    if items:
        for item in items:
            # Format the "Reorder" value as "True" or "False"
            reorder_value = "True" if item[9] else "False"
            tree.insert(
                "", "end", values=item[:9] + (reorder_value,)
            )  # Append formatted "Reorder" value


def add_item_to_database(
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
    tree,
):
    # Validate and add the item to the database
    try:
        inwards = int(inwards)
        outwards = int(outwards)
        current_stock = int(current_stock)
    except ValueError:
        messagebox.showerror(
            "Error", "Invalid input for numeric fields. Item not added."
        )
        return

    # Connect to the database
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    # Check if the item code or item description already exists
    cursor.execute("SELECT item_code FROM inventory WHERE item_code=?", (item_code,))
    existing_item_code = cursor.fetchone()
    cursor.execute(
        "SELECT item_description FROM inventory WHERE item_description=?",
        (item_description,),
    )
    existing_item_description = cursor.fetchone()

    if existing_item_code:
        messagebox.showerror(
            "Error", f"Item with Item Code {item_code} already exists."
        )
        conn.close()
        return

    if existing_item_description:
        messagebox.showerror(
            "Error", f"Item with Item Description '{item_description}' already exists."
        )
        conn.close()
        return

    # Insert the new item into the database
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

    messagebox.showinfo("Success", f"Added item '{item_description}' to the inventory.")

    # Refresh the inventory Treeview after adding a new item
    refresh_inventory_tree(tree)


def create_add_item_tab(notebook, tree):
    # Create a new tab for adding an item
    tab = ttk.Frame(notebook)
    notebook.add(tab, text="Add Item")

    # Add input fields and labels for item information
    pady_top = 20  # Adjust this value as needed for the desired top padding
    padx_left = 55  # Adjust this value as needed for the desired left padding

    item_code_label = tk.Label(tab, text="Item Code:")
    item_code_entry = tk.Entry(tab)
    item_description_label = tk.Label(tab, text="Item Description:")
    item_description_entry = tk.Entry(tab)
    category_label = tk.Label(tab, text="Category:")
    category_entry = tk.Entry(tab)
    subcategory_label = tk.Label(tab, text="Subcategory:")
    subcategory_entry = tk.Entry(tab)
    unit_label = tk.Label(tab, text="Unit:")
    unit_entry = tk.Entry(tab)
    brand_label = tk.Label(tab, text="Brand (Optional):")
    brand_entry = tk.Entry(tab)
    inwards_label = tk.Label(tab, text="Inwards:")
    inwards_entry = tk.Entry(tab)
    outwards_label = tk.Label(tab, text="Outwards:")
    outwards_entry = tk.Entry(tab)
    current_stock_label = tk.Label(tab, text="Current Stock:")
    current_stock_entry = tk.Entry(tab)
    reorder_label = tk.Label(tab, text="Reorder (True/False):")
    reorder_entry = tk.Entry(tab)

    # Set text alignment to left for labels
    for label in [
        item_code_label,
        item_description_label,
        category_label,
        subcategory_label,
        unit_label,
        brand_label,
        inwards_label,
        outwards_label,
        current_stock_label,
        reorder_label,
    ]:
        label.configure(justify="left")

    # Create a button to add the item
    add_button = tk.Button(
        tab,
        text="Add Item",
        command=lambda: add_item_to_database(
            item_code_entry.get(),
            item_description_entry.get(),
            category_entry.get(),
            subcategory_entry.get(),
            unit_entry.get(),
            brand_entry.get(),
            inwards_entry.get(),
            outwards_entry.get(),
            current_stock_entry.get(),
            reorder_entry.get().lower() == "true",
            tree,
        ),
    )

    item_code_label.grid(
        row=0, column=0, pady=(pady_top, 0), padx=(padx_left, 0), sticky="w"
    )
    item_code_entry.grid(row=0, column=1, pady=(pady_top, 0))
    item_description_label.grid(
        row=1, column=0, pady=(0, 0), padx=(padx_left, 0), sticky="w"
    )
    item_description_entry.grid(row=1, column=1, pady=(0, 0))
    category_label.grid(row=2, column=0, pady=(0, 0), padx=(padx_left, 0), sticky="w")
    category_entry.grid(row=2, column=1, pady=(0, 0))
    subcategory_label.grid(
        row=3, column=0, pady=(0, 0), padx=(padx_left, 0), sticky="w"
    )
    subcategory_entry.grid(row=3, column=1, pady=(0, 0))
    unit_label.grid(row=4, column=0, pady=(0, 0), padx=(padx_left, 0), sticky="w")
    unit_entry.grid(row=4, column=1, pady=(0, 0))
    brand_label.grid(row=5, column=0, pady=(0, 0), padx=(padx_left, 0), sticky="w")
    brand_entry.grid(row=5, column=1, pady=(0, 0))
    inwards_label.grid(row=7, column=0, pady=(0, 0), padx=(padx_left, 0), sticky="w")
    inwards_entry.grid(row=7, column=1, pady=(0, 0))
    outwards_label.grid(row=8, column=0, pady=(0, 0), padx=(padx_left, 0), sticky="w")
    outwards_entry.grid(row=8, column=1, pady=(0, 0))
    current_stock_label.grid(
        row=9, column=0, pady=(0, 0), padx=(padx_left, 0), sticky="w"
    )
    current_stock_entry.grid(row=9, column=1, pady=(0, 0))
    reorder_label.grid(row=10, column=0, pady=(0, 0), padx=(padx_left, 0), sticky="w")
    reorder_entry.grid(row=10, column=1, pady=(0, 0))
    add_button.grid(row=11, columnspan=2, pady=(pady_top, 0), padx=(padx_left, 0))


def create_view_inventory_tab(notebook):
    # Create a new tab for viewing inventory
    tab = ttk.Frame(notebook)
    notebook.add(tab, text="View Inventory")

    # Create a Treeview widget for displaying inventory items
    tree = ttk.Treeview(
        tab,
        columns=(
            "Item Code",
            "Item Description",
            "Category",
            "Subcategory",
            "Unit",
            "Brand",
            "Inwards",
            "Outwards",
            "Current Stock",
            "Reorder",
        ),
        show="headings",
    )

    # Define column headings
    tree.heading("Item Code", text="Item Code", anchor="center")
    tree.heading("Item Description", text="Item Description", anchor="center")
    tree.heading("Category", text="Category", anchor="center")
    tree.heading("Subcategory", text="Subcategory", anchor="center")
    tree.heading("Unit", text="Unit", anchor="center")
    tree.heading("Brand", text="Brand", anchor="center")  # Added "Brand" heading
    tree.heading("Inwards", text="Inwards", anchor="center")
    tree.heading("Outwards", text="Outwards", anchor="center")
    tree.heading("Current Stock", text="Current Stock", anchor="center")
    tree.heading("Reorder", text="Reorder", anchor="center")

    # Adjust column widths
    tree.column("Item Code", width=80, anchor="center")
    tree.column("Item Description", width=250, anchor="center")
    tree.column("Category", width=120, anchor="center")
    tree.column("Subcategory", width=150, anchor="center")
    tree.column("Unit", width=70, anchor="center")
    tree.column("Brand", width=100, anchor="center")
    tree.column("Inwards", width=70, anchor="center")
    tree.column("Outwards", width=70, anchor="center")
    tree.column("Current Stock", width=80, anchor="center")
    tree.column(
        "Reorder", width=80, anchor="center"
    )  # Adjust width for the "Reorder" column

    # Connect to the database
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    # Retrieve all items from the database
    cursor.execute("SELECT * FROM inventory")
    items = cursor.fetchall()

    # Close the connection
    conn.close()

    if items:
        for item in items:
            # Format the "Reorder" value as "True" or "False"
            reorder_value = "True" if item[9] else "False"
            tree.insert(
                "", "end", values=item[:9] + (reorder_value,)
            )  # Append formatted "Reorder" value

    tree.pack(fill=tk.BOTH, expand=True)

    return tree  # Return the tree widget


def delete_item_from_database(item_code, tree):
    # Delete the item from the database
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    # Check if the item with the given item code exists
    cursor.execute("SELECT item_code FROM inventory WHERE item_code=?", (item_code,))
    existing_item = cursor.fetchone()

    if existing_item:
        cursor.execute("DELETE FROM inventory WHERE item_code=?", (item_code,))
        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success", f"Item with Item Code {item_code} has been deleted."
        )
    else:
        conn.close()
        messagebox.showerror(
            "Error", f"Item with Item Code {item_code} does not exist."
        )

    # Refresh the inventory Treeview after deleting an item
    refresh_inventory_tree(tree)


def create_delete_item_tab(notebook, tree):
    # Create a new tab for deleting an item
    tab = ttk.Frame(notebook)
    notebook.add(tab, text="Delete Item")

    # Add input fields and labels for item code
    item_code_delete_label = tk.Label(tab, text="Item Code to Delete:")
    item_code_delete_entry = tk.Entry(tab)

    # Set text alignment to left for labels
    item_code_delete_label.configure(justify="left")

    # Create a button to delete the item
    delete_button = tk.Button(
        tab,
        text="Delete Item",
        command=lambda: delete_item_from_database(item_code_delete_entry.get(), tree),
    )

    item_code_delete_label.grid(row=0, column=0, pady=(20, 0), padx=(55, 0), sticky="w")
    item_code_delete_entry.grid(row=0, column=1, pady=(20, 0))
    delete_button.grid(row=1, columnspan=2, pady=(20, 0), padx=(55, 0))


def main():
    # Create the main window
    root = tk.Tk()
    root.title("Inventory Management System")
    root.geometry("1270x600")

    # Create a notebook widget for tabs
    notebook = ttk.Notebook(root)
    # Create the starting page
    start_frame = create_start_page(root, notebook)

    # Create tabs for different functionality
    tree = create_view_inventory_tab(notebook)  # Assign the created tree widget
    create_add_item_tab(notebook, tree)
    create_delete_item_tab(notebook, tree)  # Pass the "tree" to the delete tab

    # Start the GUI main loop
    root.mainloop()


if __name__ == "__main__":
    main()
