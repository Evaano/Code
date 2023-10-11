import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Create or connect to the SQLite database with case-insensitive collation
conn = sqlite3.connect('inventory.db')
conn.execute('PRAGMA case_sensitive_like = OFF')  # Ensure case-insensitive behavior
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

def back_to_main_menu(window):
    window.destroy()  # Destroy the current window
    root.deiconify()

def add_item():
    def add_item_to_database():
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

        # Validate and add the item to the database
        try:
            inwards = int(inwards)
            outwards = int(outwards)
            current_stock = int(current_stock)
        except ValueError:
            messagebox.showerror("Error", "Invalid input for numeric fields. Item not added.")
            return

        # Insert the new item into the database
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

    # Create a popup dialog for adding an item
    add_item_dialog = tk.Toplevel(root)
    add_item_dialog.title("Add New Item")

    # Add input fields and labels for item information
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

    # Place input fields, labels, and the button in the dialog
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

def update_item():
    def update_item_in_database():
        item_code = item_code_entry.get()

        # Connect to the database
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()

        # Check if the item code exists in the database
        cursor.execute("SELECT item_code FROM inventory WHERE item_code=?", (item_code,))
        existing_item = cursor.fetchone()

        if existing_item:
            # Fetch the existing item details
            cursor.execute("SELECT * FROM inventory WHERE item_code=?", (item_code,))
            existing_item_details = cursor.fetchone()

            item_description = item_description_entry.get() or existing_item_details[1]
            category = category_entry.get() or existing_item_details[2]
            subcategory = subcategory_entry.get() or existing_item_details[3]
            unit = unit_entry.get() or existing_item_details[4]
            brand = brand_entry.get() or existing_item_details[5]
            sto_code = sto_code_entry.get() or existing_item_details[6]

            try:
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

    # Create a popup dialog for updating an item
    update_item_dialog = tk.Toplevel(root)
    update_item_dialog.title("Update Item")

    # Add input fields and labels for item information
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

    # Place input fields, labels, and the button in the dialog
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

def delete_item():
    def delete_item_from_database():
        item_code = item_code_entry.get()

        # Connect to the database
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()

        # Check if the item exists in the database
        cursor.execute("SELECT item_description FROM inventory WHERE item_code=?", (item_code,))
        item = cursor.fetchone()

        if item:
            item_description = item[0]
            # Delete the item from the database
            cursor.execute("DELETE FROM inventory WHERE item_code=?", (item_code,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Deleted item {item_description} from the inventory.")
            delete_item_dialog.destroy()
        else:
            conn.close()
            messagebox.showerror("Error", f"Item with item code {item_code} not found in the inventory.")

    # Create a popup dialog for deleting an item
    delete_item_dialog = tk.Toplevel(root)
    delete_item_dialog.title("Delete Item")

    # Add input fields and labels for item code
    item_code_label = tk.Label(delete_item_dialog, text="Item Code:")
    item_code_entry = tk.Entry(delete_item_dialog)

    # Create a button to delete the item
    delete_button = tk.Button(delete_item_dialog, text="Delete Item", command=delete_item_from_database)

    # Place input fields, labels, and the button in the dialog
    item_code_label.pack()
    item_code_entry.pack()
    delete_button.pack()

def view_inventory():
    # Create a new window for viewing inventory
    view_inventory_window = tk.Toplevel(root)
    view_inventory_window.title("View Inventory")

    # Create a Treeview widget for displaying inventory items
    tree = ttk.Treeview(view_inventory_window, columns=("Item Code", "Item Description", "Category", "Subcategory", "Unit", "Brand", "STO Code", "Inwards", "Outwards", "Current Stock", "Reorder"), show="headings")

    # Define column headings
    tree.heading("Item Code", text="Item Code", anchor="center")
    tree.heading("Item Description", text="Item Description", anchor="center")
    tree.heading("Category", text="Category", anchor="center")
    tree.heading("Subcategory", text="Subcategory", anchor="center")
    tree.heading("Unit", text="Unit", anchor="center")
    tree.heading("Brand", text="Brand", anchor="center")  # Added "Brand" heading
    tree.heading("STO Code", text="STO Code", anchor="center")
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
    tree.column("STO Code", width=70, anchor="center")
    tree.column("Inwards", width=70, anchor="center")
    tree.column("Outwards", width=70, anchor="center")
    tree.column("Current Stock", width=80, anchor="center")
    tree.column("Reorder", width=80, anchor="center")  # Adjust width for the "Reorder" column

    # Connect to the database
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    # Retrieve all items from the database
    cursor.execute("SELECT * FROM inventory")
    items = cursor.fetchall()

    # Close the connection
    conn.close()

    if items:
        for item in items:
            # Format the "Reorder" value as "True" or "False"
            reorder_value = "True" if item[10] else "False"
            tree.insert("", "end", values=item[:10] + (reorder_value,))  # Append formatted "Reorder" value

    tree.pack(fill=tk.BOTH, expand=True)

    back_button = tk.Button(view_inventory_window, text="Back to Main Menu", command=lambda: back_to_main_menu(view_inventory_window))
    back_button.pack()

def search_item_by_name():
    def search_items(event=None):
        search_term = search_name_entry.get().strip().lower()

        # Connect to the database
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()

        # Search for items with descriptions containing the search term (case-insensitive)
        cursor.execute("SELECT * FROM inventory WHERE LOWER(item_description) LIKE ?", ('%' + search_term + '%',))
        items = cursor.fetchall()

        # Close the connection
        conn.close()

        # Clear previous search results
        for row in tree.get_children():
            tree.delete(row)

        if items:
            for item in items:
                # Format the "Reorder" value as "True" or "False"
                reorder_value = "True" if item[10] else "False"
                tree.insert("", "end", values=item[:10] + (reorder_value,))  # Append formatted "Reorder" value

    # Create a new window for searching items
    search_item_window = tk.Toplevel(root)
    search_item_window.title("Search Items by Name")

    # Create a frame for search input and results
    frame = tk.Frame(search_item_window)
    frame.pack(padx=0, pady=10)

    # Create an input field and label for search term
    search_name_label = tk.Label(frame, text="Item Name:")
    search_name_entry = tk.Entry(frame)

    # Bind the Enter key to initiate the search
    search_name_entry.bind("<Return>", search_items)

    # Create a Treeview widget for displaying search results
    tree = ttk.Treeview(frame, columns=("Item Code", "Item Description", "Category", "Subcategory", "Unit", "Brand", "STO Code", "Inwards", "Outwards", "Current Stock", "Reorder"), show="headings")

    # Define column headings
    tree.heading("#1", text="Item Code", anchor="center")
    tree.heading("#2", text="Item Description", anchor="center")
    tree.heading("#3", text="Category", anchor="center")
    tree.heading("#4", text="Subcategory", anchor="center")
    tree.heading("#5", text="Unit", anchor="center")
    tree.heading("#6", text="Brand", anchor="center")  # Added "Brand" heading
    tree.heading("#7", text="STO Code", anchor="center")
    tree.heading("#8", text="Inwards", anchor="center")
    tree.heading("#9", text="Outwards", anchor="center")
    tree.heading("#10", text="Current Stock", anchor="center")
    tree.heading("#11", text="Reorder", anchor="center")

    # Adjust column widths
    tree.column("#1", width=80, anchor="center")
    tree.column("#2", width=250, anchor="center")
    tree.column("#3", width=120, anchor="center")
    tree.column("#4", width=150, anchor="center")
    tree.column("#5", width=70, anchor="center")
    tree.column("#6", width=100, anchor="center")
    tree.column("#7", width=70, anchor="center")
    tree.column("#8", width=70, anchor="center")
    tree.column("#9", width=80, anchor="center")
    tree.column("#10", width=80, anchor="center")
    tree.column("#11", width=80, anchor="center")

    # Place widgets in the frame
    search_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    search_name_entry.grid(row=0, column=1, padx=5, pady=5)
    tree.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    # Create a frame for the "Back" button
    back_frame = tk.Frame(search_item_window)
    back_frame.pack()

    # Create a "Back" button to return to the main menu
    back_button = tk.Button(back_frame, text="Back to Main Menu", command=lambda: back_to_main_menu(search_item_window))
    back_button.pack()


# Create the main window
root = tk.Tk()
root.title("Inventory Management System")

# Set the initial size of the window (width x height)
root.geometry("800x600")  # Adjust the dimensions as needed

# Create buttons for each operation
add_button = tk.Button(root, text="Add Item", command=add_item)
update_button = tk.Button(root, text="Update Item", command=update_item)
delete_button = tk.Button(root, text="Delete Item", command=delete_item)
view_button = tk.Button(root, text="View Inventory", command=view_inventory)
search_button = tk.Button(root, text="Search by Name", command=search_item_by_name)
exit_button = tk.Button(root, text="Exit", command=root.quit)

# Place buttons on the window
add_button.pack()
update_button.pack()
delete_button.pack()
view_button.pack()
search_button.pack()
exit_button.pack()

# Start the GUI main loop
root.mainloop()