import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import pyperclip

# Subcategories dictionary
subcategories = {
    "General Items": [
        "General Items",
        "Printed Items",
        "Stationaries",
        "Toners, Cartridges, and Drums",
    ],
    "Medical Items": [
        "Dental Consumables",
        "Dialysis",
        "Laboratory Consumables",
        "Laboratory Test Kits",
        "Medical Consumables",
        "Medical Instruments",
        "Oncology Items",
        "Pharmaceuticals",
        "Radiology",
    ],
    "Narcotics": ["Controlled Drugs"],
}

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


# Show the inventory app
def show_inventory_app(start_frame, notebook):
    start_frame.pack_forget()
    notebook.pack(fill="both", expand=True)


# Create a frame for the starting page
def create_start_page(root, notebook):
    start_frame = ttk.Frame(root)
    start_frame.pack(fill="both", expand=True)

    # Load and resize the image
    original_image = Image.open("start_image.png")
    resized_image = original_image.resize((300, 300))
    image = ImageTk.PhotoImage(resized_image)
    image_label = tk.Label(start_frame, image=image)
    image_label.image = image
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


# Refresh the inventory Treeview
def refresh_inventory_tree(tree):
    for item in tree.get_children():
        tree.delete(item)
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    items = cursor.fetchall()
    conn.close()
    if items:
        for item in items:
            reorder_value = "True" if item[9] else "False"
            tree.insert("", "end", values=item[:9] + (reorder_value,))


# Add an item to the database
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
    tree,
):
    try:
        inwards = int(inwards)
        outwards = int(outwards)
    except ValueError:
        messagebox.showerror(
            "Error", "Invalid input for numeric fields. Item not added."
        )
        return
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
    refresh_inventory_tree(tree)


# Create a tab for adding a new item
def create_add_item_tab(notebook, tree):
    tab = ttk.Frame(notebook)
    notebook.add(tab, text="Add New Item")
    pady_top = 20
    padx_left = 55
    item_code_label = tk.Label(tab, text="Item Code:")
    item_code_entry = tk.Entry(tab)
    item_code_entry = tk.Entry(tab)
    max_item_code = get_max_item_code() + 1
    item_code_entry.insert(0, max_item_code)
    item_description_label = tk.Label(tab, text="Item Description:")
    item_description_entry = tk.Entry(tab)
    category_label = tk.Label(tab, text="Category:")
    category_combobox = ttk.Combobox(
        tab,
        values=[
            "General Items",
            "Medical Items",
            "Narcotics",
        ],
        width="17",
    )
    category_combobox.set("General Items")
    subcategory_label = tk.Label(tab, text="Subcategory:")
    subcategory_combobox = ttk.Combobox(
        tab, values=subcategories["General Items"], width="17"
    )
    subcategory_combobox.set("General Items")

    def update_subcategories(event):
        selected_category = category_combobox.get()
        subcategory_combobox["values"] = subcategories[selected_category]
        subcategory_combobox.set(subcategories[selected_category][0])

    category_combobox.bind("<<ComboboxSelected>>", update_subcategories)
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
    add_button = tk.Button(
        tab,
        text="Add Item",
        command=lambda: add_item_to_database(
            item_code_entry.get(),
            item_description_entry.get(),
            category_combobox.get(),
            subcategory_combobox.get(),
            unit_entry.get(),
            brand_entry.get(),
            inwards_entry.get(),
            outwards_entry.get(),
            reorder_entry.get().lower() == "true",
            tree,
        ),
    )
    clear_button = tk.Button(
        tab,
        text="Clear",
        command=lambda: clear_input_fields(
            item_code_entry,
            item_description_entry,
            category_combobox,
            subcategory_combobox,
            unit_entry,
            brand_entry,
            inwards_entry,
            outwards_entry,
            reorder_entry,
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
    category_combobox.grid(row=2, column=1, pady=(0, 0))
    subcategory_label.grid(
        row=3, column=0, pady=(0, 0), padx=(padx_left, 0), sticky="w"
    )
    subcategory_combobox.grid(row=3, column=1, pady=(0, 0))
    unit_label.grid(row=4, column=0, pady=(0, 0), padx=(padx_left, 0), sticky="w")
    unit_entry.grid(row=4, column=1, pady=(0, 0))
    brand_label.grid(row=5, column=0, pady=(0, 0), padx=(padx_left, 0), sticky="w")
    brand_entry.grid(row=5, column=1, pady=(0, 0))
    inwards_label.grid(row=6, column=0, pady=(0, 0), padx=(padx_left, 0), sticky="w")
    inwards_entry.grid(row=6, column=1, pady=(0, 0))
    outwards_label.grid(row=7, column=0, pady=(0, 0), padx=(padx_left, 0), sticky="w")
    outwards_entry.grid(row=7, column=1, pady=(0, 0))
    reorder_label.grid(row=9, column=0, pady=(0, 0), padx=(padx_left, 0), sticky="w")
    reorder_entry.grid(row=9, column=1, pady=(0, 0))
    clear_button.grid(row=11, columnspan=2, pady=(pady_top, 0), padx=(80, 0))
    add_button.grid(row=11, columnspan=4, pady=(pady_top, 0), padx=(235, 0))
    return tab


# Get the maximum item code
def get_max_item_code():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(item_code) FROM inventory")
    result = cursor.fetchone()
    conn.close()
    max_item_code = result[0] if result[0] is not None else 0
    return int(max_item_code)


def clear_input_fields(
    item_code_entry,
    item_description_entry,
    category_combobox,
    subcategory_combobox,
    unit_entry,
    brand_entry,
    inwards_entry,
    outwards_entry,
    reorder_entry,
):
    # Clear all the input fields
    item_code_entry.delete(0, "end")
    item_description_entry.delete(0, "end")
    category_combobox.set("General Items")
    subcategory_combobox.set("General Items")
    unit_entry.delete(0, "end")
    brand_entry.delete(0, "end")
    inwards_entry.delete(0, "end")
    outwards_entry.delete(0, "end")
    reorder_entry.delete(0, "end")

    # Get the maximum item code and increment it by 1
    max_item_code = get_max_item_code() + 1

    # Set the default value of the "Item Code" entry
    item_code_entry.insert(0, max_item_code)


def create_view_inventory_tab(notebook):
    # Create a new tab for viewing inventory
    tab = ttk.Frame(notebook)
    notebook.add(tab, text="View Inventory")
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

    # Create an entry field for searching items
    search_entry = tk.Entry(tab, width=40)
    search_entry.grid(row=0, column=3, pady=20, padx=20, columnspan=3)

    def filter_items(event):
        # Get the search keyword from the entry field
        keyword = search_entry.get().strip().lower()

        # Clear the existing items in the Treeview
        for item in tree.get_children():
            tree.delete(item)

        # Connect to the database
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()

        # Retrieve all items from the database that match the search keyword
        cursor.execute(
            "SELECT * FROM inventory WHERE lower(item_description) LIKE ?",
            ("%" + keyword + "%",),
        )
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

    # Bind the filter_items function to the key release event
    search_entry.bind("<KeyRelease>", filter_items)

    print("Refreshing Treeview")
    # Call the refresh_inventory_tree function to populate the Treeview initially
    refresh_inventory_tree(tree)

    # Bind Ctrl+C to copy selected cell
    tree.bind("<Control-c>", lambda event: copy_selected_cell(event, tree))

    # Add the Treeview using the grid manager
    tree.grid(row=1, column=0, columnspan=6, padx=20, pady=10, sticky="nsew")

    # Configure grid row and column weights to make the Treeview expand properly
    tab.grid_rowconfigure(1, weight=1)
    tab.grid_columnconfigure(0, weight=1)

    return tree  # Return the tree widget and search_entry widget


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


def update_item_in_database(
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
    # Validate and update the item in the database
    try:
        inwards = int(inwards)
        outwards = int(outwards)
    except ValueError:
        messagebox.showerror(
            "Error", "Invalid input for numeric fields. Item not updated."
        )
        return

    # Calculate the "Current Stock" as "Inwards - Outwards"
    current_stock = inwards - outwards

    # Connect to the database
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    # Update the item in the database
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

    messagebox.showinfo("Success", f"Item with Item Code {item_code} updated.")

    refresh_inventory_tree(tree)


def get_item_descriptions_from_database():
    # Connect to your SQLite database (replace 'inventory.db' with your actual database file)
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    # Execute a query to fetch all item descriptions
    cursor.execute("SELECT item_description FROM inventory")
    descriptions = [row[0] for row in cursor.fetchall()]

    # Close the database connection
    conn.close()

    return descriptions


def search_item_and_fill_fields(
    selected_option,
    item_code_entry,
    item_description_entry,
    category_combobox,
    subcategory_combobox,
    unit_entry,
    brand_entry,
    inwards_entry,
    outwards_entry,
    current_stock_entry,
    reorder_entry,
):
    item_to_update = selected_option  # Use the selected option

    # Connect to the database
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    # Check if the item with the given item code or item name exists
    cursor.execute(
        "SELECT * FROM inventory WHERE item_code=? OR item_description=?",
        (item_to_update, item_to_update),
    )
    existing_item = cursor.fetchone()

    if existing_item:
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
        ) = existing_item
        item_code_entry.delete(0, tk.END)
        item_code_entry.insert(0, item_code)
        item_description_entry.delete(0, tk.END)
        item_description_entry.insert(0, item_description)
        category_combobox.set(category)
        subcategory_combobox.set(subcategory)
        unit_entry.delete(0, tk.END)
        unit_entry.insert(0, unit)
        brand_entry.delete(0, tk.END)
        brand_entry.insert(0, brand)
        inwards_entry.delete(0, tk.END)
        inwards_entry.insert(0, inwards)
        outwards_entry.delete(0, tk.END)
        outwards_entry.insert(0, outwards)
        current_stock_entry.delete(0, tk.END)
        current_stock_entry.insert(0, current_stock)
        reorder_entry.delete(0, tk.END)
        reorder_entry.insert(0, "True" if reorder else "False")
    else:
        conn.close()
        # Handle the case where the item is not found.

    conn.close()


def create_update_item_tab(notebook, tree):
    # Create a new tab for updating item details
    tab = ttk.Frame(notebook)
    notebook.add(tab, text="Update Item")

    # Create a frame for labels, entries, and buttons
    input_frame = tk.Frame(tab)
    input_frame.grid()

    # Add a "Select Item" label and an input field
    select_item_label = tk.Label(input_frame, text="Select Item:")
    select_item_label.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="w")
    item_var = tk.StringVar()
    item_entry = tk.Entry(input_frame, textvariable=item_var)
    item_entry.grid(row=0, column=0, padx=(100, 0), pady=(20, 0), sticky="w")

    # Create a StringVar to store the selected option
    selected_option = tk.StringVar()

    # Add an OptionMenu
    item_option_menu = ttk.OptionMenu(input_frame, selected_option, "", "")
    item_option_menu.grid()

    # Define an event handler for the StringVar
    def on_item_var_change(*args):
        selected_item = item_var.get()
        search_item_and_fill_fields(
            selected_item,
            item_code_entry,
            item_description_entry,
            category_combobox,
            subcategory_combobox,
            unit_entry,
            brand_entry,
            inwards_entry,
            outwards_entry,
            current_stock_entry,
            reorder_entry,
        )

    # Bind the event handler to the StringVar
    item_var.trace("w", on_item_var_change)

    # Add labels for item fields and corresponding entry widgets
    item_code_label = tk.Label(input_frame, text="Item Code:")
    item_code_entry = tk.Entry(input_frame)
    item_description_label = tk.Label(input_frame, text="Item Description:")
    item_description_entry = tk.Entry(input_frame)
    category_label = tk.Label(input_frame, text="Category:")
    category_combobox = ttk.Combobox(
        input_frame, values=["General Items", "Medical Items", "Narcotics"], width="17"
    )
    subcategory_label = tk.Label(input_frame, text="Subcategory:")
    subcategory_combobox = ttk.Combobox(
        input_frame, values=subcategories["General Items"], width="17"
    )

    def update_subcategories(event):
        # Update subcategories Combobox based on the selected category
        selected_category = category_combobox.get()
        subcategory_combobox["values"] = subcategories[selected_category]
        subcategory_combobox.set(
            subcategories[selected_category][0]
        )  # Set the first subcategory as default

    category_combobox.bind("<<ComboboxSelected>>", update_subcategories)
    unit_label = tk.Label(input_frame, text="Unit:")
    unit_entry = tk.Entry(input_frame)
    brand_label = tk.Label(input_frame, text="Brand (Optional):")
    brand_entry = tk.Entry(input_frame)
    inwards_label = tk.Label(input_frame, text="Inwards:")
    inwards_entry = tk.Entry(input_frame)
    outwards_label = tk.Label(input_frame, text="Outwards:")
    outwards_entry = tk.Entry(input_frame)
    current_stock_entry = tk.Entry(input_frame)
    reorder_label = tk.Label(input_frame, text="Reorder (True/False):")
    reorder_entry = tk.Entry(input_frame)

    # Create buttons for updating and deleting items
    update_button = tk.Button(
        input_frame,
        text="Update Item",
        command=lambda: update_item_in_database(
            item_code_entry.get(),
            item_description_entry.get(),
            category_combobox.get(),
            subcategory_combobox.get(),
            unit_entry.get(),
            brand_entry.get(),
            inwards_entry.get(),
            outwards_entry.get(),
            current_stock_entry.get(),
            reorder_entry.get().lower() == "true",
            tree,
        ),
    )

    delete_button = tk.Button(
        input_frame,
        text="Delete Item",
        command=lambda: delete_item_from_database(item_code_entry.get(), tree),
    )

    # Place labels, entry widgets, and buttons in the input frame
    item_code_label.grid(row=0, column=4, padx=(20, 0), pady=(10, 0), sticky="w")
    item_code_entry.grid(row=0, column=5, padx=(20, 0), pady=(10, 0), sticky="w")
    item_description_label.grid(row=1, column=4, padx=(20, 0), pady=(0, 0), sticky="w")
    item_description_entry.grid(row=1, column=5, padx=(20, 0), pady=(0, 0), sticky="w")
    category_label.grid(row=2, column=4, padx=(20, 0), pady=(7, 0), sticky="w")
    category_combobox.grid(row=2, column=5, padx=(20, 0), pady=(7, 0), sticky="w")
    subcategory_label.grid(row=3, column=4, padx=(20, 0), pady=(7, 0), sticky="w")
    subcategory_combobox.grid(row=3, column=5, padx=(20, 0), pady=(7, 0), sticky="w")
    unit_label.grid(row=4, column=4, padx=(20, 0), pady=(7, 0), sticky="w")
    unit_entry.grid(row=4, column=5, padx=(20, 0), pady=(7, 0), sticky="w")
    brand_label.grid(row=5, column=4, padx=(20, 0), pady=(7, 0), sticky="w")
    brand_entry.grid(row=5, column=5, padx=(20, 0), pady=(7, 0), sticky="w")
    inwards_label.grid(row=6, column=4, padx=(20, 0), pady=(7, 0), sticky="w")
    inwards_entry.grid(row=6, column=5, padx=(20, 0), pady=(7, 0), sticky="w")
    outwards_label.grid(row=7, column=4, padx=(20, 0), pady=(7, 0), sticky="w")
    outwards_entry.grid(row=7, column=5, padx=(20, 0), pady=(7, 0), sticky="w")
    reorder_label.grid(row=8, column=4, padx=(20, 0), pady=(7, 0), sticky="w")
    reorder_entry.grid(row=8, column=5, padx=(20, 0), pady=(7, 0), sticky="w")
    delete_button.grid(row=9, column=4, padx=(20, 0), pady=(20, 0), sticky="w")
    update_button.grid(row=9, column=5, padx=(75, 0), pady=(20, 0), sticky="w")

    # Populate the Treeview with items from the database
    refresh_items_tree(tree)
    return tab, item_var, selected_option, item_option_menu


def update_option_menu(item_var, item_option_menu, item_descriptions):
    def update_option_menu_internal(*args):
        # Get the current text from the input field
        current_text = item_var.get()

        # Filter item descriptions that match the current text
        filtered_descriptions = [
            desc for desc in item_descriptions if current_text.lower() in desc.lower()
        ]

        # Update the OptionMenu with the filtered descriptions
        item_option_menu["menu"].delete(0, "end")
        for desc in filtered_descriptions:
            item_option_menu["menu"].add_command(
                label=desc, command=tk._setit(item_var, desc)
            )

        # Disable the OptionMenu if the input field is empty
        item_option_menu["state"] = "disabled" if not current_text else "normal"

    return update_option_menu_internal


def copy_selected_cell(event, tree):
    selected_item = tree.item(tree.selection())
    if selected_item:
        selected_cell = selected_item["values"]
        selected_cell_text = "\t".join(str(cell) for cell in selected_cell)
        pyperclip.copy(selected_cell_text)


def create_update_inwards_tab(notebook, tree):
    # Create a new tab for updating inwards quantities
    tab = ttk.Frame(notebook)
    notebook.add(tab, text="Update Inwards")

    # Create a label and entry field for item description with autocomplete functionality
    item_description_label = tk.Label(tab, text="Item Description:")
    item_description_var = tk.StringVar()
    item_description_entry = tk.Entry(tab, textvariable=item_description_var, width=40)

    item_description_label.grid(row=2, column=0, padx=10, pady=2, sticky="w")
    item_description_entry.grid(row=2, column=1, padx=10, pady=2, sticky="w")

    # Create a Treeview widget to display the list of items
    items_tree = ttk.Treeview(
        tab,
        columns=("Item Description", "Inwards"),
        show="headings",
    )

    # Define column headings
    items_tree.heading("Item Description", text="Item Description", anchor="center")
    items_tree.heading("Inwards", text="Inwards", anchor="center")

    # Adjust column widths
    items_tree.column("Item Description", width=300, anchor="center")
    items_tree.column("Inwards", width=100, anchor="center")

    items_tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)

    def populate_item_description(event):
        # Populate the item description field when an item is selected in the Treeview
        selected_item = items_tree.item(items_tree.selection())
        item_description = selected_item["values"][0]
        item_description_var.set(item_description)

        # Set the inwards entry with the inwards quantity of the selected item
        inwards_quantity = selected_item["values"][1]
        inwards_quantity_var.set(inwards_quantity)

        # Focus on the inwards quantity entry box when an item is selected
        inwards_entry.focus_set()

        # Move the cursor to the end of the inwards quantity entry
        inwards_entry.icursor("end")

    # Bind the populate_item_description function to the Treeview selection event
    items_tree.bind("<<TreeviewSelect>>", populate_item_description)

    # Add input fields and labels for updating inwards quantities
    inwards_label = tk.Label(tab, text="Inwards Quantity:")
    inwards_quantity_var = tk.StringVar()
    inwards_entry = tk.Entry(tab, textvariable=inwards_quantity_var)

    def move_to_next_item():
        # Get the selected item's index
        selected_index = items_tree.index(items_tree.selection())

        if selected_index is not None:
            next_index = selected_index + 1
            if next_index < len(items_tree.get_children()):
                # Focus on the next item in the Treeview
                items_tree.selection_set(items_tree.get_children()[next_index])
                items_tree.focus(items_tree.get_children()[next_index])

                # Populate the inwards entry with the inwards quantity of the next item
                next_item = items_tree.item(items_tree.get_children()[next_index])
                inwards_quantity_var.set(next_item["values"][1])

    def search_items(event):
        # Get the search keyword from the item description field
        keyword = item_description_var.get().strip().lower()

        # Clear the existing items in the Treeview
        for item in items_tree.get_children():
            items_tree.delete(item)

        # Connect to the database
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()

        # Retrieve items from the database that match the search keyword
        cursor.execute(
            "SELECT item_description, inwards FROM inventory WHERE lower(item_description) LIKE ?",
            ("%" + keyword + "%",),
        )
        items = cursor.fetchall()

        # Close the connection
        conn.close()

        if items:
            for item in items:
                items_tree.insert("", "end", values=(item[0], item[1]))

    # Bind the search_items function to the item description field's key release event
    item_description_entry.bind("<KeyRelease>", search_items)

    def update_inwards_button_click(event=None):
        item_description = item_description_var.get()
        inwards_quantity = inwards_entry.get()

        if inwards_quantity:  # Check if the input is not empty
            update_inwards_quantity(item_description, inwards_quantity, tree)
            move_to_next_item()

    # Bind the Enter key press event to the inwards quantity entry box
    inwards_entry.bind("<Return>", update_inwards_button_click)

    inwards_label.grid(row=3, column=0, padx=10, pady=2, sticky="w")
    inwards_entry.grid(row=3, column=1, padx=10, pady=2, sticky="w")

    update_inwards_button = tk.Button(
        tab,
        text="Update Inwards",
        command=update_inwards_button_click  # Bind this function to the button
    )

    inwards_label.grid(row=3, column=0, padx=10, pady=2, sticky="w")
    inwards_entry.grid(row=3, column=1, padx=10, pady=2, sticky="w")
    update_inwards_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    # Populate the items_tree with items from your database
    refresh_items_tree(items_tree)

    return tab


def refresh_items_tree(items_tree):
    # Clear the existing items in the Treeview
    for item in items_tree.get_children():
        items_tree.delete(item)

    # Connect to the database
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    # Retrieve all items from the database
    cursor.execute("SELECT item_description, inwards FROM inventory")
    items = cursor.fetchall()

    conn.close()

    if items:
        for item in items:
            items_tree.insert("", "end", values=(item[0], item[1]))


def update_inwards_quantity(item_description, inwards_quantity, tree):
    try:
        inwards_quantity = int(inwards_quantity)
    except ValueError:
        messagebox.showerror(
            "Error", "Invalid input for inwards quantity. Please enter a valid number."
        )
        return

    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    # Check if the item with the given description exists in the inventory
    cursor.execute(
        "SELECT item_code FROM inventory WHERE item_description=?", (item_description,)
    )
    existing_item = cursor.fetchone()

    if existing_item:
        # Retrieve the inwards, outwards, and current_stock values for the item
        cursor.execute(
            "SELECT inwards, outwards, current_stock FROM inventory WHERE item_code=?",
            (existing_item[0],),
        )
        inwards, outwards, current_stock = cursor.fetchone()

        # Calculate the new inwards and current_stock values
        new_inwards = inwards + inwards_quantity
        new_current_stock = new_inwards - outwards

        # Update the inventory with the new values
        cursor.execute(
            "UPDATE inventory SET inwards=?, current_stock=? WHERE item_code=?",
            (new_inwards, new_current_stock, existing_item[0]),
        )
        conn.commit()
        conn.close()

        # Display a success message
        messagebox.showinfo(
            "Success", f"Inwards quantity updated for Item Code {existing_item[0]}."
        )

        refresh_items_tree(tree)
        refresh_inventory_tree(tree)
    else:
        conn.close()
        # Item not found error message
        messagebox.showerror(
            "Error", f"Item with Item Description '{item_description}' not found."
        )


def main():
    root = tk.Tk()  # Create the main window
    root.title("Inventory Management System")
    root.geometry("1270x600")

    notebook = ttk.Notebook(root)  # Create a notebook widget for tabs
    start_frame = create_start_page(root, notebook)  # Create the starting page

    tree = create_view_inventory_tab(notebook)  # Create "View Inventory" tab
    create_add_item_tab(notebook, tree)  # Create "Add Item" tab

    # Create "Update Item" tab and obtain relevant variables
    (
        update_item_tab,
        item_var,
        selected_option,
        item_option_menu,
    ) = create_update_item_tab(notebook, tree)
    create_update_inwards_tab(notebook, tree)  # Create "Update Inwards" tab

    item_descriptions = (
        get_item_descriptions_from_database()
    )  # Retrieve item descriptions from the database

    # Create update_option_menu function with required parameters
    update_option_menu_func = update_option_menu(
        item_var, item_option_menu, item_descriptions
    )

    item_var.trace_add(
        "write", update_option_menu_func
    )  # Add trace on item_var for OptionMenu updates
    refresh_inventory_tree(tree)  # Refresh the inventory Treeview initially

    root.mainloop()  # Start the GUI main loop


if __name__ == "__main__":
    main()
