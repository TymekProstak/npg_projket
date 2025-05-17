import json
import tkinter as tk
from tkinter import messagebox

class FlashcardInterface:
    def __init__(self, json_path, index, callbacks):
        """
        json_path: ścieżka do pliku JSON z fiszkami
        index: numer fiszki (0-based)
        callbacks: słownik funkcji dla klawiszy:
            {
                'quit': func,
                'next': func,
                'prev': func,
                'toggle': func,
                'yes': func,
                'no': func
            }
        """
        # Wczytanie fiszek
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie można wczytać pliku JSON:\n{e}")
            return

        # Spłaszczanie struktury (jeśli JSON ma poziomy)
        if isinstance(data, dict):
            flashcards = []
            for level in data.values():
                flashcards.extend(level)
        elif isinstance(data, list):
            flashcards = data
        else:
            messagebox.showerror("Błąd", "Nieznany format JSON")
            return

        if not (0 <= index < len(flashcards)):
            messagebox.showerror("Błąd", "Index fiszki poza zakresem")
            return

        self.card = flashcards[index]
        self.callbacks = callbacks

        # Inicjalizacja okna
        self.root = tk.Tk()
        self.root.title("Flashcard Viewer (Tkinter)")
        self.root.geometry("600x400")
        self.root.bind("<Key>", self.on_key)

        # Etykiety
        self.pol_label = tk.Label(self.root, text=self.card["polski"], font=("Arial", 24), wraplength=580)
        self.pol_label.pack(expand=True, pady=20)

        self.eng_label = tk.Label(self.root, text="", font=("Arial", 20), fg="blue", wraplength=580)
        self.eng_label.pack()

        # Instrukcja
        instr_text = "←: Poprzednia  →: Następna  Spacja: Toggle  Y: Yes  N: No  Q: Quit"
        self.instr_label = tk.Label(self.root, text=instr_text, font=("Arial", 12), fg="gray")
        self.instr_label.pack(side="bottom", pady=10)

        self.show_translation = False

    def on_key(self, event):
        key = event.keysym.lower()
        if key == "q":
            self.callbacks.get('quit', lambda: None)()
            self.root.destroy()
        elif key in ("right", "n"):  # strzałka w prawo lub 'n'
            self.callbacks.get('next', lambda: None)()
        elif key in ("left",):     # strzałka w lewo
            self.callbacks.get('prev', lambda: None)()
        elif key == "space":
            self.toggle_translation()
            self.callbacks.get('toggle', lambda: None)()
        elif key == "y":
            self.callbacks.get('yes', lambda: None)()
        elif key == "n":
            self.callbacks.get('no', lambda: None)()

    def toggle_translation(self):
        if not self.show_translation:
            self.eng_label.config(text=self.card["angielski"])
            self.show_translation = True
        else:
            self.eng_label.config(text="")
            self.show_translation = False

    def run(self):
        self.root.mainloop()

# Przykład użycia:
if __name__ == "__main__":
    def on_quit(): print("Quit")
    def on_next(): print("Next")
    def on_prev(): print("Prev")
    def on_toggle(): print("Toggle")
    def on_yes(): print("Yes")
    def on_no(): print("No")

    json_path = "fiszki_B2_unikalne.json"  # przykładowa ścieżka
    index = 0  # wyświetl pierwszą fiszkę

    callbacks = {
        'quit': on_quit,
        'next': on_next,
        'prev': on_prev,
        'toggle': on_toggle,
        'yes': on_yes,
        'no': on_no
    }

    app = FlashcardInterface(json_path, index, callbacks)
    app.run()
