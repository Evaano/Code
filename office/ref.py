import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Define the main application class
class InventoryApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Inventory Management System")
        self.geometry("800x600")

        # Create instances of frames for different functionalities
        self.main_menu_frame = MainMenu(self)
        self.add_item_frame = AddItem(self)
        self.update_item_frame = UpdateItem(self)
        self.delete_item_frame = DeleteItem(self)
        self.view_inventory_frame = ViewInventory(self)
        self.search_item_frame = SearchItem(self)

        # Show the main menu frame initially
        self.show_main_menu()

    def show_main_menu(self):
        # Hide all frames and display the main menu frame
        self.hide_all_frames()
        self.main_menu_frame.pack()

    def hide_all_frames(self):
        # Helper function to hide all frames
        self.main_menu_frame.pack_forget()
        self.add_item_frame.pack_forget()
        self.update_item_frame.pack_forget()
        self.delete_item_frame.pack_forget()
        self.view_inventory_frame.pack_forget()
        self.search_item_frame.pack_forget()

# Frame for the main menu
class MainMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Create buttons to navigate to different functionalities
        self.add_button = tk.Button(self, text="Add Item", command=master.add_item_frame.pack)
        self.update_button = tk.Button(self, text="Update Item", command=master.update_item_frame.pack)
        self.delete_button = tk.Button(self, text="Delete Item", command=master.delete_item_frame.pack)
        self.view_button = tk.Button(self, text="View Inventory", command=master.view_inventory_frame.pack)
        self.search_button = tk.Button(self, text="Search by Name", command=master.search_item_frame.pack)
        self.exit_button = tk.Button(self, text="Exit", command=master.quit)

        # Pack the buttons for the main menu
        self.add_button.pack()
        self.update_button.pack()
        self.delete_button.pack()
        self.view_button.pack()
        self.search_button.pack()
        self.exit_button.pack()

# Frame for adding items to the database
class AddItem(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Input fields and labels for item information
        self.item_code_label = tk.Label(self, text="Item Code:")
        self.item_code_entry = tk.Entry(self)
        self.item_description_label = tk.Label(self, text="Item Description:")
        self.item_description_entry = tk.Entry(self)
        self.category_label = tk.Label(self, text="Category:")
        self.category_entry = tk.Entry(self)
        self.subcategory_label = tk.Label(self, text="Sub Category:")
        self.subcategory_entry = tk.Entry(self)
        self.unit_label = tk.Label(self, text="Unit:")
        self.unit_entry = tk.Entry(self)
        self.brand_label = tk.Label(self, text="Brand:")
        self.brand_entry = tk.Entry(self)
        self.sto_code_label = tk.Label(self, text="STO Code:")
        self.sto_code_entry = tk.Entry(self)
        self.inwards_label = tk.Label(self, text="Inwards:")
        self.inwards_entry = tk.Entry(self)
        self.outwards_label = tk.Label(self, text="Outwards:")
        self.outwards_entry = tk.Entry(self)
        self.current_stock_label = tk.Label(self, text="Current Stock:")
        self.current_stock_entry = tk.Entry(self)
        self.reorder_label = tk.Label(self, text="Reorder:")
        self.reorder_entry = tk.Entry(self)

        # Button to add an item and button to go back to the main menu
        self.add_button = tk.Button(self, text="Add Item", command=self.add_item_to_database)
        self.back_button = tk.Button(self, text="Back to Main Menu", command=master.show_main_menu)

        # Pack input fields, labels, and buttons
        self.item_code_label.pack()
        self.item_code_entry.pack()
        self.item_description_label.pack()
        self.item_description_entry.pack()
        self.category_label.pack()
        self.category_entry.pack()
        self.subcategory_label.pack()
        self.subcategory_entry.pack()
        self.unit_label.pack()
        self.unit_entry.pack()
        self.brand_label.pack()
        self.brand_entry.pack()
        self.sto_code_label.pack()
        self.sto_code_entry.pack()
        self.inwards_label.pack()
        self.inwards_entry.pack()
        self.outwards_label.pack()
        self.outwards_entry.pack()
        self.current_stock_label.pack()
        self.current_stock_entry.pack()
        self.reorder_label.pack()
        self.reorder_entry.pack()
        self.add_button.pack()
        self.back_button.pack()

    def add_item_to_database(self):
        # Get input values from entry fields
        item_code = self.item_code_entry.get()
        item_description = self.item_description_entry.get()
        category = self.category_entry.get()
        subcategory = self.subcategory_entry.get()
        unit = self.unit_entry.get()
        brand = self.brand_entry.get()
        sto_code = self.sto_code_entry.get()
        inwards = self.inwards_entry.get()
        outwards = self.outwards_entry.get()
        current_stock = self.current_stock_entry.get()
        reorder = self.reorder_entry.get()

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

        # Display a success message box
        messagebox.showinfo("Success", f"Added item {item_code} to the inventory.")

        # Clear input fields
        self.item_code_entry.delete(0, tk.END)
        self.item_description_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.subcategory_entry.delete(0, tk.END)
        self.unit_entry.delete(0, tk.END)
        self.brand_entry.delete(0, tk.END)
        self.sto_code_entry.delete(0, tk.END)
        self.inwards_entry.delete(0, tk.END)
        self.outwards_entry.delete(0, tk.END)
        self.current_stock_entry.delete(0, tk.END)
        self.reorder_entry.delete(0, tk.END)

# Frame for updating items in the database
class UpdateItem(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Input fields and labels for updating
        self.item_code_label = tk.Label(self, text="Item Code:")
        self.item_code_entry = tk.Entry(self)
        self.new_item_description_label = tk.Label(self, text="New Item Description:")
        self.new_item_description_entry = tk.Entry(self)

        # Button to update an item and button to go back to the main menu
        self.update_button = tk.Button(self, text="Update Item", command=self.update_item_in_database)
        self.back_button = tk.Button(self, text="Back to Main Menu", command=master.show_main_menu)

        # Pack input fields, labels, and buttons
        self.item_code_label.pack()
        self.item_code_entry.pack()
        self.new_item_description_label.pack()
        self.new_item_description_entry.pack()
        self.update_button.pack()
        self.back_button.pack()

    def update_item_in_database(self):
        # Get input values from entry fields
        item_code = self.item_code_entry.get()
        new_item_description = self.new_item_description_entry.get()

        # Validate and update the item in the database
        try:
            # Connect to the database
            with sqlite3.connect('inventory.db') as conn:
                cursor = conn.cursor()
                # Perform the update operation in the database (similar to AddItem)
                cursor.execute('''
                    UPDATE inventory
                    SET item_description = ?
                    WHERE item_code = ?
                ''', (new_item_description, item_code))
                conn.commit()

            # Display a success message box if the update is successful
            messagebox.showinfo("Success", f"Updated item {item_code} in the inventory.")

            # Clear input fields
            self.item_code_entry.delete(0, tk.END)
            self.new_item_description_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update item: {str(e)}")

# Frame for deleting items from the database
class DeleteItem(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Input field and label
        self.item_code_label = tk.Label(self, text="Item Code:")
        self.item_code_entry = tk.Entry(self)

        # Button to delete an item and button to go back to the main menu
        self.delete_button = tk.Button(self, text="Delete Item", command=self.delete_item_from_database)
        self.back_button = tk.Button(self, text="Back to Main Menu", command=master.show_main_menu)

        # Pack input field, label, and buttons
        self.item_code_label.pack()
        self.item_code_entry.pack()
        self.delete_button.pack()
        self.back_button.pack()

    def delete_item_from_database(self):
        # Get input value from entry field
        item_code = self.item_code_entry.get()

        # Delete the item from the database based on the item code
        try:
            with sqlite3.connect('inventory.db') as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM inventory WHERE item_code=?", (item_code,))
                conn.commit()

            # Display a success message box
            messagebox.showinfo("Success", f"Deleted item {item_code} from the inventory.")

            # Clear input field
            self.item_code_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete item: {str(e)}")

# Frame for viewing inventory
class ViewInventory(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Create a Treeview widget to display the inventory
        self.tree = ttk.Treeview(self, columns=("Item Code", "Item Description", "Category", "Subcategory", "Unit", "Brand", "STO Code", "Inwards", "Outwards", "Current Stock", "Reorder"), show="headings")

        # Define column headings
        columns = [
            "Item Code", "Item Description", "Category", "Subcategory", "Unit", "Brand", "STO Code", "Inwards",
            "Outwards", "Current Stock", "Reorder"
        ]

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)  # Adjust the column width as needed

        # Connect to the database and retrieve inventory data
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory")
        inventory_data = cursor.fetchall()
        conn.close()

        # Populate the Treeview widget with inventory data
        for row in inventory_data:
            self.tree.insert("", "end", values=row)

        # Add a scrollbar for the Treeview
        self.tree_scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.tree_scroll.set)

        # Pack the Treeview and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        self.tree_scroll.pack(side="right", fill="y")

        # Back button to go to the main menu
        self.back_button = tk.Button(self, text="Back to Main Menu", command=master.show_main_menu)
        self.back_button.pack()

# Frame for searching items by name
class SearchItem(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Search input field and label
        self.search_name_label = tk.Label(self, text="Item Name:")
        self.search_name_entry = tk.Entry(self)
        self.search_name_entry.bind("<Return>", self.search_items)

        # Create a Treeview widget to display search results
        self.tree = ttk.Treeview(self, columns=("Item Code", "Item Description", "Category", "Subcategory", "Unit", "Brand", "STO Code", "Inwards", "Outwards", "Current Stock", "Reorder"), show="headings")

        # Define column headings
        columns = [
            "Item Code", "Item Description", "Category", "Subcategory", "Unit", "Brand", "STO Code", "Inwards",
            "Outwards", "Current Stock", "Reorder"
        ]

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)  # Adjust the column width as needed

        # Search button and back button to go to the main menu
        self.search_button = tk.Button(self, text="Search", command=self.search_items)
        self.back_button = tk.Button(self, text="Back to Main Menu", command=master.show_main_menu)

        # Pack search input field, label, Treeview, buttons
        self.search_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.search_name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.tree.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        self.search_button.grid(row=2, column=0, padx=5, pady=5)
        self.back_button.grid(row=2, column=1, padx=5, pady=5)

    def search_items(self, event=None):
        search_term = self.search_name_entry.get().strip().lower()

        # Connect to the database and search for items
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory WHERE LOWER(item_description) LIKE ?", ('%' + search_term + '%',))
        search_results = cursor.fetchall()
        conn.close()

        # Clear previous search results from the Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Populate the Treeview with search results
        for row in search_results:
            self.tree.insert("", "end", values=row)

if __name__ == "__main__":
    app = InventoryApp()
    app.mainloop()