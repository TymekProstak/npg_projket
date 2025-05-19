import json
import tkinter as tk
from tkinter import messagebox

class FlashcardInterface:
    def __init__(self, json_path, index, callbacks, mode='pl-en'):
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
        mode: 'pl-en' lub 'en-pl'
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
        self.mode = mode  # Ustawienie trybu

        # Inicjalizacja okna
        self.root = tk.Tk()
        self.root.title("Flashcard Viewer (Tkinter)")
        self.root.geometry("600x400")
        self.root.bind("<Key>", self.on_key)

        # Etykiety
        self.front_label = tk.Label(self.root, text=self.get_front_text(),
                                    font=("Arial", 24), wraplength=580)
        self.front_label.pack(expand=True, pady=20)

        self.back_label = tk.Label(self.root, text="", font=("Arial", 20),
                                   fg="blue", wraplength=580)
        self.back_label.pack()

        # Instrukcja
        instr = (
            "←: Poprzednia  →: Następna  "
            "Spacja : Tłumaczenie  Y: Umiem  N: Nie umiem  Q: Quit"
        )
        self.instr_label = tk.Label(self.root, text=instr,
                                    font=("Arial", 12), fg="gray")
        self.instr_label.pack(side="bottom", pady=10)

        self.show_back = False

    def get_front_text(self):
        # Zwraca tekst na froncie karty wg trybu
        if self.mode == 'pl-en':
            return self.card['polski']
        else:  # 'en-pl'
            return self.card['angielski']

    def get_back_text(self):
        # Zwraca tekst na odwrocie karty wg trybu
        if self.mode == 'pl-en':
            return self.card['angielski']
        else:
            return self.card['polski']

    def on_key(self, event):
        key = event.keysym.lower()
        if key == 'q':
            self.callbacks.get('quit', lambda: None)()
            self.root.destroy()
        elif key in ('right', 'n'):
            self.callbacks.get('next', lambda: None)()
        elif key == 'left':
            self.callbacks.get('prev', lambda: None)()
        elif key == 'space':
            self.toggle()
            self.callbacks.get('toggle', lambda: None)()
        elif key == 'y':
            self.callbacks.get('yes', lambda: None)()
        elif key == 'n':
            self.callbacks.get('no', lambda: None)()

    def toggle(self):
        # Przełącza widok front/back
        if not self.show_back:
            self.back_label.config(text=self.get_back_text())
            self.show_back = True
        else:
            self.back_label.config(text='')
            self.show_back = False

    def run(self):
        self.root.mainloop()

# TEST
if __name__ == '__main__':
    def on_quit(): print('Quit')
    def on_next(): print('Next')
    def on_prev(): print('Prev')
    def on_toggle(): print('Toggle')
    def on_yes(): print('Yes')
    def on_no(): print('No')

    json_path = 'fiszki_B2_unikalne.json'
    index = 0
    mode = 'pl-en'  # lub 'pl-en'

    callbacks = {
        'quit': on_quit,
        'next': on_next,
        'prev': on_prev,
        'toggle': on_toggle,
        'yes': on_yes,
        'no': on_no
    }

    app = FlashcardInterface(json_path, index, callbacks, mode)
    app.run()
