import tkinter as tk
from tkinter import ttk, messagebox

class SelectionWindow:
    def __init__(self, on_submit_callback):
        self.root = tk.Tk()
        self.root.title("Wybór ustawień")
        self.root.geometry("400x300")

        self.on_submit_callback = on_submit_callback

        # Wybór poziomu trudności
        tk.Label(self.root, text="Poziom trudności:").pack(pady=(10, 0))
        self.level_var = tk.StringVar(value="B2")
        ttk.Combobox(self.root, textvariable=self.level_var, values=["B2", "C1", "C2"]).pack()

        # Wybór kierunku tłumaczenia
        tk.Label(self.root, text="Kierunek tłumaczenia:").pack(pady=(10, 0))
        self.mode_var = tk.StringVar(value="pl-en")
        ttk.Combobox(self.root, textvariable=self.mode_var, values=["pl-en", "en-pl"]).pack()

        # Wybór trybu
        tk.Label(self.root, text="Tryb pracy:").pack(pady=(10, 0))
        self.type_var = tk.StringVar(value="nauka")
        ttk.Combobox(self.root, textvariable=self.type_var, values=["nauka", "sprawdzian", "powtórka"]).pack()

        # Przycisk rozpoczęcia
        tk.Button(self.root, text="Rozpocznij", command=self.submit).pack(pady=20)

    def submit(self):
        level = self.level_var.get()
        mode = self.mode_var.get()
        typ = self.type_var.get()

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
