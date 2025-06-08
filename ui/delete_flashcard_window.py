import tkinter as tk
from tkinter import ttk, messagebox
import json

class DeleteFlashcardWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Usuwanie fiszki")
        self.root.geometry("800x600")  # Set a fixed size for the window
        self.root.configure(bg="#f5f5f5")

        # Title
        tk.Label(
            self.root,
            text="Usuń fiszkę",
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

        # Flashcard list
        tk.Label(
            self.root,
            text="Wybierz fiszkę do usunięcia:",
            font=("Arial", 16),
            bg="#f5f5f5",
            fg="#333333",
        ).pack(anchor="w", padx=20, pady=(10, 0))
        self.flashcard_listbox = tk.Listbox(self.root, font=("Arial", 14), height=10)
        self.flashcard_listbox.pack(fill="both", padx=20, pady=(0, 20))

        # Delete button
        tk.Button(
            self.root,
            text="Usuń fiszkę",
            command=self.delete_flashcard,
            font=("Arial", 16, "bold"),
            bg="#d9534f",
            fg="#ffffff",
            activebackground="#c9302c",
            activeforeground="#ffffff",
            relief="raised",
            bd=2,
        ).pack(pady=(10, 20))

        # Load flashcards when level is selected
        self.level_var.trace("w", self.load_flashcards)

    def load_flashcards(self, *args):
        level = self.level_var.get()
        file_map = {
            "B2": "data/fiszki_B2_unikalne.json",
            "C1": "data/fiszki_C1_unikalne.json",
            "C2": "data/fiszki_C2_unikalne.json",
        }
        file_path = file_map.get(level)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.flashcards = json.load(f)
        except FileNotFoundError:
            self.flashcards = []

        self.flashcard_listbox.delete(0, tk.END)
        for i, flashcard in enumerate(self.flashcards):
            self.flashcard_listbox.insert(tk.END, f"{i + 1}. {flashcard['polski']} - {flashcard['angielski']}")

    def delete_flashcard(self):
        selected_index = self.flashcard_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Błąd", "Proszę wybrać fiszkę do usunięcia.")
            return

        index = selected_index[0]
        del self.flashcards[index]

        level = self.level_var.get()
        file_map = {
            "B2": "data/fiszki_B2_unikalne.json",
            "C1": "data/fiszki_C1_unikalne.json",
            "C2": "data/fiszki_C2_unikalne.json",
        }
        file_path = file_map.get(level)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.flashcards, f, ensure_ascii=False, indent=4)

        messagebox.showinfo("Sukces", "Fiszka została usunięta!")
        self.load_flashcards()

    def run(self):
        self.root.mainloop()