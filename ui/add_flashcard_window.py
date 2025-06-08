import tkinter as tk
from tkinter import ttk, messagebox
import json

class AddFlashcardWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Dodawanie fiszki")
        self.root.geometry("800x600")  # Set a fixed size for the window
        self.root.configure(bg="#f5f5f5")

        # Title
        tk.Label(
            self.root,
            text="Dodaj nową fiszkę",
            font=("Arial", 24, "bold"),
            bg="#f5f5f5",
            fg="#333333",
        ).pack(pady=(20, 10))

        # Difficulty level selection
        tk.Label(
            self.root,
            text="Poziom trudności:",
            font=("Arial", 16),
            bg="#f5f5f5",
            fg="#333333",
        ).pack(anchor="w", padx=20, pady=(10, 0))
        self.level_var = tk.StringVar(value="B2")
        ttk.Combobox(
            self.root,
            textvariable=self.level_var,
            values=["B2", "C1", "C2"],
            font=("Arial", 14),
        ).pack(fill="x", padx=20, pady=(0, 20))

        # Polish word input
        tk.Label(
            self.root,
            text="Polskie tłumaczenie:",
            font=("Arial", 16),
            bg="#f5f5f5",
            fg="#333333",
        ).pack(anchor="w", padx=20, pady=(10, 0))
        self.polish_entry = tk.Entry(self.root, font=("Arial", 14))
        self.polish_entry.pack(fill="x", padx=20, pady=(0, 20))

        # English word input
        tk.Label(
            self.root,
            text="Angielskie tłumaczenie:",
            font=("Arial", 16),
            bg="#f5f5f5",
            fg="#333333",
        ).pack(anchor="w", padx=20, pady=(10, 0))
        self.english_entry = tk.Entry(self.root, font=("Arial", 14))
        self.english_entry.pack(fill="x", padx=20, pady=(0, 20))

        # Submit button
        tk.Button(
            self.root,
            text="Dodaj fiszkę",
            command=self.add_flashcard,
            font=("Arial", 16, "bold"),
            bg="#007acc",
            fg="#ffffff",
            activebackground="#005f99",
            activeforeground="#ffffff",
            relief="raised",
            bd=2,
        ).pack(pady=(20, 10))

    def add_flashcard(self):
        level = self.level_var.get()
        polish = self.polish_entry.get()
        english = self.english_entry.get()

        if not (level and polish and english):
            messagebox.showerror("Błąd", "Proszę wypełnić wszystkie pola.")
            return

        # Save the flashcard to the appropriate JSON file
        file_map = {
            "B2": "data/fiszki_B2_unikalne.json",
            "C1": "data/fiszki_C1_unikalne.json",
            "C2": "data/fiszki_C2_unikalne.json",
        }
        file_path = file_map.get(level)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        data.append({"polski": polish, "angielski": english})

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        messagebox.showinfo("Sukces", "Fiszka została dodana!")
        self.root.destroy()

    def run(self):
        self.root.mainloop()