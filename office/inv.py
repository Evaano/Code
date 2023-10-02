# Import necessary libraries
import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Connect to the SQLite database or create one if it doesn't exist
conn = sqlite3.connect('inventory.db')
# Set case-insensitive search for the database
conn.execute('PRAGMA case_sensitive_like = OFF')
# Create the 'inventory' table if it doesn't exist
conn.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        item_code TEXT PRIMARY KEY,
        item_description TEXT COLLATE NOCASE,
        category TEXT COLLATE NOCASE,
        subcategory TEXT COLLATE NOCASE,
        unit TEXT COLLATE NOCASE,
        brand TEXT COLLATE NOCASE,
        sto_code TEXT COLLATE NOCASE,
        inwards INTEGER,
        outwards INTEGER,
        current_stock INTEGER,
        reorder INTEGER
    )
''')
conn.commit()
conn.close()

# Function to add a new item to the inventory
def add_item():
    def add_item_to_database():
        # Get data from input fields
        item_code = item_code_entry.get()
        item_description = item_description_entry.get()
        category = category_entry.get()
        subcategory = subcategory_entry.get()
        unit = unit_entry.get()
        brand = brand_entry.get()
        sto_code = sto_code_entry.get()
        inwards = inwards_entry.get()
        outwards = outwards_entry.get()
        current_stock = current_stock_entry.get()
        reorder = reorder_entry.get().lower() == 'true'

        try:
            # Convert numeric fields to integers
            inwards = int(inwards)
            outwards = int(outwards)
            current_stock = int(current_stock)
        except ValueError:
            messagebox.showerror("Error", "Invalid input for numeric fields. Item not added.")
            return

        # Connect to the database and insert the item
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO inventory
            (item_code, item_description, category, subcategory, unit, brand, sto_code, inwards, outwards, current_stock, reorder)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (item_code, item_description, category, subcategory, unit, brand, sto_code, inwards, outwards, current_stock, reorder))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Added item {item_description} to the inventory.")
        add_item_dialog.destroy()

    # Create a new dialog window for adding an item
    add_item_dialog = tk.Toplevel(root)
    add_item_dialog.title("Add New Item")

    # Create labels and entry fields for item details
    item_code_label = tk.Label(add_item_dialog, text="Item Code:")
    item_code_entry = tk.Entry(add_item_dialog)
    item_description_label = tk.Label(add_item_dialog, text="Item Description:")
    item_description_entry = tk.Entry(add_item_dialog)
    category_label = tk.Label(add_item_dialog, text="Category:")
    category_entry = tk.Entry(add_item_dialog)
    subcategory_label = tk.Label(add_item_dialog, text="Subcategory:")
    subcategory_entry = tk.Entry(add_item_dialog)
    unit_label = tk.Label(add_item_dialog, text="Unit:")
    unit_entry = tk.Entry(add_item_dialog)
    brand_label = tk.Label(add_item_dialog, text="Brand (Optional):")
    brand_entry = tk.Entry(add_item_dialog)
    sto_code_label = tk.Label(add_item_dialog, text="STO Code (Optional):")
    sto_code_entry = tk.Entry(add_item_dialog)
    inwards_label = tk.Label(add_item_dialog, text="Inwards:")
    inwards_entry = tk.Entry(add_item_dialog)
    outwards_label = tk.Label(add_item_dialog, text="Outwards:")
    outwards_entry = tk.Entry(add_item_dialog)
    current_stock_label = tk.Label(add_item_dialog, text="Current Stock:")
    current_stock_entry = tk.Entry(add_item_dialog)
    reorder_label = tk.Label(add_item_dialog, text="Reorder (True/False):")
    reorder_entry = tk.Entry(add_item_dialog)

    # Create a button to add the item
    add_button = tk.Button(add_item_dialog, text="Add Item", command=add_item_to_database)

    # Grid layout for labels, entry fields, and the button
    item_code_label.grid(row=0, column=0)
    item_code_entry.grid(row=0, column=1)
    item_description_label.grid(row=1, column=0)
    item_description_entry.grid(row=1, column=1)
    category_label.grid(row=2, column=0)
    category_entry.grid(row=2, column=1)
    subcategory_label.grid(row=3, column=0)
    subcategory_entry.grid(row=3, column=1)
    unit_label.grid(row=4, column=0)
    unit_entry.grid(row=4, column=1)
    brand_label.grid(row=5, column=0)
    brand_entry.grid(row=5, column=1)
    sto_code_label.grid(row=6, column=0)
    sto_code_entry.grid(row=6, column=1)
    inwards_label.grid(row=7, column=0)
    inwards_entry.grid(row=7, column=1)
    outwards_label.grid(row=8, column=0)
    outwards_entry.grid(row=8, column=1)
    current_stock_label.grid(row=9, column=0)
    current_stock_entry.grid(row=9, column=1)
    reorder_label.grid(row=10, column=0)
    reorder_entry.grid(row=10, column=1)
    add_button.grid(row=11, columnspan=2)

# Function to update an existing item in the inventory
def update_item():
    def update_item_in_database():
        item_code = item_code_entry.get()

        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()

        cursor.execute("SELECT item_code FROM inventory WHERE item_code=?", (item_code,))
        existing_item = cursor.fetchone()

        if existing_item:
            cursor.execute("SELECT * FROM inventory WHERE item_code=?", (item_code,))
            existing_item_details = cursor.fetchone()

            # Get updated data from input fields, or use existing data if fields are empty
            item_description = item_description_entry.get() or existing_item_details[1]
            category = category_entry.get() or existing_item_details[2]
            subcategory = subcategory_entry.get() or existing_item_details[3]
            unit = unit_entry.get() or existing_item_details[4]
            brand = brand_entry.get() or existing_item_details[5]
            sto_code = sto_code_entry.get() or existing_item_details[6]

            try:
                # Convert numeric fields to integers, or use existing data if fields are empty
                inwards = int(inwards_entry.get() or existing_item_details[7])
                outwards = int(outwards_entry.get() or existing_item_details[8])
                current_stock = int(current_stock_entry.get() or existing_item_details[9])
            except ValueError:
                messagebox.showerror("Error", "Invalid input for numeric fields. Item not updated.")
                conn.close()
                return

            reorder = reorder_entry.get() or existing_item_details[10]

            # Update the item in the database
            cursor.execute('''
                UPDATE inventory
                SET item_description=?, category=?, subcategory=?, unit=?, brand=?, sto_code=?, inwards=?, outwards=?, current_stock=?, reorder=?
                WHERE item_code=?
            ''', (item_description, category, subcategory, unit, brand, sto_code, inwards, outwards, current_stock, reorder, item_code))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Updated item {item_code} in the inventory.")
            update_item_dialog.destroy()
        else:
            conn.close()
            messagebox.showerror("Error", f"Item with item code {item_code} not found in the inventory.")

    # Create a new dialog window for updating an item
    update_item_dialog = tk.Toplevel(root)
    update_item_dialog.title("Update Item")

    # Create labels and entry fields for item details
    item_code_label = tk.Label(update_item_dialog, text="Item Code:")
    item_code_entry = tk.Entry(update_item_dialog)
    item_description_label = tk.Label(update_item_dialog, text="Item Description:")
    item_description_entry = tk.Entry(update_item_dialog)
    category_label = tk.Label(update_item_dialog, text="Category:")
    category_entry = tk.Entry(update_item_dialog)
    subcategory_label = tk.Label(update_item_dialog, text="Subcategory:")
    subcategory_entry = tk.Entry(update_item_dialog)
    unit_label = tk.Label(update_item_dialog, text="Unit:")
    unit_entry = tk.Entry(update_item_dialog)
    brand_label = tk.Label(update_item_dialog, text="Brand (Optional):")
    brand_entry = tk.Entry(update_item_dialog)
    sto_code_label = tk.Label(update_item_dialog, text="STO Code (Optional):")
    sto_code_entry = tk.Entry(update_item_dialog)
    inwards_label = tk.Label(update_item_dialog, text="Inwards:")
    inwards_entry = tk.Entry(update_item_dialog)
    outwards_label = tk.Label(update_item_dialog, text="Outwards:")
    outwards_entry = tk.Entry(update_item_dialog)
    current_stock_label = tk.Label(update_item_dialog, text="Current Stock:")
    current_stock_entry = tk.Entry(update_item_dialog)
    reorder_label = tk.Label(update_item_dialog, text="Reorder (True/False):")
    reorder_entry = tk.Entry(update_item_dialog)

    # Create a button to update the item
    update_button = tk.Button(update_item_dialog, text="Update Item", command=update_item_in_database)

    # Grid layout for labels, entry fields, and the button
    item_code_label.grid(row=0, column=0)
    item_code_entry.grid(row=0, column=1)
    item_description_label.grid(row=1, column=0)
    item_description_entry.grid(row=1, column=1)
    category_label.grid(row=2, column=0)
    category_entry.grid(row=2, column=1)
    subcategory_label.grid(row=3, column=0)
    subcategory_entry.grid(row=3, column=1)
    unit_label.grid(row=4, column=0)
    unit_entry.grid(row=4, column=1)
    brand_label.grid(row=5, column=0)
    brand_entry.grid(row=5, column=1)
    sto_code_label.grid(row=6, column=0)
    sto_code_entry.grid(row=6, column=1)
    inwards_label.grid(row=7, column=0)
    inwards_entry.grid(row=7, column=1)
    outwards_label.grid(row=8, column=0)
    outwards_entry.grid(row=8, column=1)
    current_stock_label.grid(row=9, column=0)
    current_stock_entry.grid(row=9, column=1)
    reorder_label.grid(row=10, column=0)
    reorder_entry.grid(row=10, column=1)
    update_button.grid(row=11, columnspan=2)

# Function to delete an item from the inventory
def delete_item():
    def delete_item_from_database():
        item_code = item_code_entry.get()

        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()

        cursor.execute("SELECT item_description FROM inventory WHERE item_code=?", (item_code,))
        item = cursor.fetchone()

        if item:
            item_description = item[0]
            cursor.execute("DELETE FROM inventory WHERE item_code=?", (item_code,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Deleted item {item_description} from the inventory.")
            delete_item_dialog.destroy()
        else:
            conn.close()
            messagebox.showerror("Error", f"Item with item code {item_code} not found in the inventory.")

    # Create a new dialog window for deleting an item
    delete_item_dialog = tk.Toplevel(root)
    delete_item_dialog.title("Delete Item")

    # Create a label and an entry field for item code
    item_code_label = tk.Label(delete_item_dialog, text="Item Code:")
    item_code_entry = tk.Entry(delete_item_dialog)

    # Create a button to delete the item
    delete_button = tk.Button(delete_item_dialog, text="Delete Item", command=delete_item_from_database)

    item_code_label.pack()
    item_code_entry.pack()
    delete_button.pack()

# Function to view the entire inventory
def view_inventory():
    view_inventory_window = tk.Toplevel(root)
    view_inventory_window.title("View Inventory")

    # Create a treeview widget to display the inventory data in a table format
    tree = ttk.Treeview(view_inventory_window, columns=("Item Code", "Item Description", "Category", "Subcategory", "Unit", "Inwards", "Outwards", "Current Stock", "Reorder"), show="headings")

    # Set column headings
    tree.heading("Item Code", text="Item Code", anchor="w")
    tree.heading("Item Description", text="Item Description", anchor="center")
    tree.heading("Category", text="Category", anchor="center")
    tree.heading("Subcategory", text="Subcategory", anchor="center")
    tree.heading("Unit", text="Unit", anchor="center")
    tree.heading("Inwards", text="Inwards", anchor="center")
    tree.heading("Outwards", text="Outwards", anchor="center")
    tree.heading("Current Stock", text="Current Stock", anchor="center")
    tree.heading("Reorder", text="Reorder", anchor="center")

    # Set column widths
    tree.column("#1", width=80, anchor="center")
    tree.column("#2", width=250, anchor="center")
    tree.column("#3", width=120, anchor="center")
    tree.column("#4", width=150, anchor="center")
    tree.column("#5", width=70, anchor="center")
    tree.column("#6", width=70, anchor="center")
    tree.column("#7", width=70, anchor="center")
    tree.column("#8", width=80, anchor="center")
    tree.column("#9", width=70, anchor="center")

    # Connect to the database and fetch all items
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    items = cursor.fetchall()
    conn.close()

    # Insert items into the treeview
    if items:
        for item in items:
            tree.insert("", "end", values=item)

    # Pack the treeview to display it
    tree.pack(fill=tk.BOTH, expand=True)

# Function to search items by name
def search_item_by_name():
    def search_items(event=None):
        search_term = search_name_entry.get().strip().lower()

        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM inventory WHERE LOWER(item_description) LIKE ?", ('%' + search_term + '%',))
        items = cursor.fetchall()

        conn.close()

        # Clear the existing items in the treeview
        for row in tree.get_children():
            tree.delete(row)

        # Insert search results into the treeview
        if items:
            for item in items:
                tree.insert("", "end", values=item)

    # Create a new dialog window for searching items by name
    search_item_window = tk.Toplevel(root)
    search_item_window.title("Search Items by Name")

    frame = tk.Frame(search_item_window)
    frame.pack(padx=0, pady=10)

    # Create a label and an entry field for item name search
    search_name_label = tk.Label(frame, text="Item Name:")
    search_name_entry = tk.Entry(frame)

    # Bind the Enter key to the search function
    search_name_entry.bind("<Return>", search_items)

    # Create a treeview widget to display search results
    tree = ttk.Treeview(frame, columns=("Item Code", "Item Description", "Category", "Subcategory", "Unit", "Inwards", "Outwards", "Current Stock", "Reorder"), show="headings")

    # Set column headings and widths
    tree.heading("#1", text="Item Code", anchor="center")
    tree.heading("#2", text="Item Description", anchor="center")
    tree.heading("#3", text="Category", anchor="center")
    tree.heading("#4", text="Subcategory", anchor="center")
    tree.heading("#5", text="Unit", anchor="center")
    tree.heading("#6", text="Inwards", anchor="center")
    tree.heading("#7", text="Outwards", anchor="center")
    tree.heading("#8", text="Current Stock", anchor="center")
    tree.heading("#9", text="Reorder", anchor="center")

    tree.column("#1", width=80, anchor="center")
    tree.column("#2", width=250, anchor="center")
    tree.column("#3", width=100, anchor="center")
    tree.column("#4", width=120, anchor="center")
    tree.column("#5", width=80, anchor="center")
    tree.column("#6", width=80, anchor="center")
    tree.column("#7", width=80, anchor="center")
    tree.column("#8", width=100, anchor="center")
    tree.column("#9", width=80, anchor="center")

    # Create a button to perform the search
    search_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    search_name_entry.grid(row=0, column=1, padx=5, pady=5)
    tree.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

# Create the main Tkinter window
root = tk.Tk()
root.title("Inventory Management System")
root.geometry("800x600")

# Create buttons for different operations
add_button = tk.Button(root, text="Add Item", command=add_item)
update_button = tk.Button(root, text="Update Item", command=update_item)
delete_button = tk.Button(root, text="Delete Item", command=delete_item)
view_button = tk.Button(root, text="View Inventory", command=view_inventory)
search_button = tk.Button(root, text="Search by Name", command=search_item_by_name)
exit_button = tk.Button(root, text="Exit", command=root.quit)

# Pack buttons to display them in the main window
add_button.pack()
update_button.pack()
delete_button.pack()
view_button.pack()
search_button.pack()
exit_button.pack()

# Start the Tkinter main loop
root.mainloop()
