import tkinter as tk
from tkinter import ttk

class ScrollableTable(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scrollable Table")

        # Create a Treeview widget
        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Age"), show="headings")

        # Define column headings
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Age", text="Age")

        # Insert sample data
        for i in range(1, 21):
            self.tree.insert("", "end", values=(i, f"Name {i}", 20 + i))

        # Create a vertical scrollbar
        yscrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=yscrollbar.set)

        # Pack the Treeview and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        yscrollbar.pack(side="right", fill="y")

if __name__ == "__main__":
    app = ScrollableTable()
    app.mainloop()