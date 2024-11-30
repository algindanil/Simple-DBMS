import tkinter as tk
from tkinter import messagebox
import requests
import json

from app import init_module

# Flask server's URL (change this to your server's URL if running locally or remotely)
BASE_URL = 'http://127.0.0.1:5000/'

class DBApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter App")
        self.db = init_module()[1]


        # Create input fields and buttons
        self.create_widgets()

    def create_widgets(self):
        # Set Key and Value
        self.key_label = tk.Label(self.root, text="Key:")
        self.key_label.grid(row=0, column=0, padx=10, pady=5)
        self.key_entry = tk.Entry(self.root, width=30)
        self.key_entry.grid(row=0, column=1, padx=10, pady=5)

        self.value_label = tk.Label(self.root, text="Value:")
        self.value_label.grid(row=1, column=0, padx=10, pady=5)
        self.value_entry = tk.Entry(self.root, width=30)
        self.value_entry.grid(row=1, column=1, padx=10, pady=5)

        self.add_button = tk.Button(self.root, text="Add Value", command=self.add_value)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Retrieve Key and Value
        self.get_key_button = tk.Button(self.root, text="Get Values for Key", command=self.get_values)
        self.get_key_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.remove_value_button = tk.Button(self.root, text="Remove Value from Key", command=self.remove_value)
        self.remove_value_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Show Database Keys
        self.show_keys_button = tk.Button(self.root, text="Show All Keys", command=self.show_keys)
        self.show_keys_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Results display area
        self.result_text = tk.Text(self.root, width=50, height=10)
        self.result_text.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        self.result_text.config(state=tk.DISABLED)

    def clear_result(self):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)

    def display_result(self, result):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, json.dumps(result, indent=4))
        self.result_text.config(state=tk.DISABLED)

    def add_value(self):
        key = self.key_entry.get()
        value = self.value_entry.get()

        if not key or not value:
            messagebox.showerror("Error", "Both key and value must be provided.")
            return

        try:
            self.db.set(key, value)
            messagebox.showinfo("Success", f"Value '{value}' added to key '{key}' successfully.")
        except:
            messagebox.showerror("Error", f"Failed to add value")

    def get_values(self):
        key = self.key_entry.get()
        if not key:
            messagebox.showerror("Error", "Please provide a key.")
            return

        # response = requests.get(f"{BASE_URL}get", params={"key": key})

        try:
            values = self.db.get(key)
            self.display_result({key: list(values)})
        except:
            messagebox.showerror(f"Error, failed to retrieve values for key '{key}'")

    def remove_value(self):
        key = self.key_entry.get()
        value = self.value_entry.get()

        if not key or not value:
            messagebox.showerror("Error", "Both key and value must be provided.")
            return

        try:
            self.db.remove_value(key, value)
            messagebox.showinfo("Success", f"Value '{value}' removed from key '{key}' successfully.")
        except:
            messagebox.showerror("Error", f"Failed to remove value")

    def show_keys(self):
        # response = requests.get(f"{BASE_URL}keys")

        try:
            keys = self.db.keys()
            self.display_result({"keys": list(keys)})
        except:
            messagebox.showerror(f"Error getting keys")


if __name__ == "__main__":
    root = tk.Tk()
    app = DBApp(root)
    root.mainloop()
