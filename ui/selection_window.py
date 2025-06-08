import tkinter as tk
from tkinter import ttk, messagebox

class SelectionWindow:
    def __init__(self, on_submit_callback, on_add_flashcard_callback, on_delete_flashcard_callback):
        self.root = tk.Tk()
        self.root.title("Wybór ustawień")
        self.root.geometry("800x600")  # Set a fixed size for the window
        self.root.configure(bg="#f5f5f5")  # Light gray background

        self.on_submit_callback = on_submit_callback
        self.on_add_flashcard_callback = on_add_flashcard_callback
        self.on_delete_flashcard_callback = on_delete_flashcard_callback

        # Main frame for content
        self.main_frame = tk.Frame(self.root, bg="#ffffff", relief="groove", bd=2)
        self.main_frame.pack(expand=True, fill="both", padx=40, pady=40)

        # Title label
        tk.Label(
            self.main_frame,
            text="Wybierz ustawienia",
            font=("Arial", 28, "bold"),
            bg="#ffffff",
            fg="#333333",
        ).pack(pady=(20, 40))

        # Difficulty level selection
        tk.Label(
            self.main_frame,
            text="Poziom trudności:",
            font=("Arial", 16),
            bg="#ffffff",
            fg="#333333",
        ).pack(anchor="w", padx=20, pady=(10, 0))
        self.level_var = tk.StringVar(value="B2")
        ttk.Combobox(
            self.main_frame,
            textvariable=self.level_var,
            values=["B2", "C1", "C2"],
            font=("Arial", 14),
        ).pack(fill="x", padx=20, pady=(0, 20))

        # Translation direction selection
        tk.Label(
            self.main_frame,
            text="Kierunek tłumaczenia:",
            font=("Arial", 16),
            bg="#ffffff",
            fg="#333333",
        ).pack(anchor="w", padx=20, pady=(10, 0))
        self.mode_var = tk.StringVar(value="pl-en")
        ttk.Combobox(
            self.main_frame,
            textvariable=self.mode_var,
            values=["pl-en", "en-pl"],
            font=("Arial", 14),
        ).pack(fill="x", padx=20, pady=(0, 20))

        # Mode selection
        tk.Label(
            self.main_frame,
            text="Tryb pracy:",
            font=("Arial", 16),
            bg="#ffffff",
            fg="#333333",
        ).pack(anchor="w", padx=20, pady=(10, 0))
        self.type_var = tk.StringVar(value="nauka")
        ttk.Combobox(
            self.main_frame,
            textvariable=self.type_var,
            values=["nauka", "sprawdzian", "powtórka", "dodawanie fiszki", "usuwanie fiszki"],
            font=("Arial", 14),
        ).pack(fill="x", padx=20, pady=(0, 20))

        # Submit button
        tk.Button(
            self.main_frame,
            text="Rozpocznij",
            command=self.submit,
            font=("Arial", 16, "bold"),
            bg="#007acc",
            fg="#ffffff",
            activebackground="#005f99",
            activeforeground="#ffffff",
            relief="raised",
            bd=2,
        ).pack(pady=(40, 20))

    def submit(self):
        level = self.level_var.get()
        mode = self.mode_var.get()
        typ = self.type_var.get()

        if typ == "dodawanie fiszki":
            self.root.destroy()
            self.on_add_flashcard_callback()
            return

        if typ == "usuwanie fiszki":
            self.root.destroy()
            self.on_delete_flashcard_callback()
            return

        if not (level and mode and typ):
            messagebox.showerror("Błąd", "Proszę wybrać wszystkie opcje.")
            return

        self.root.destroy()
        self.on_submit_callback(level, mode, typ)

    def run(self):
        self.root.mainloop()

# TEST
if __name__ == '__main__':
    def start_app(level, mode, typ):
        print("Wybrane:", level, mode, typ)
        # Tu normalnie przechodziłbyś do controller.py

    app = SelectionWindow(start_app)
    app.run()
