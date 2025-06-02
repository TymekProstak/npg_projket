import random
import tkinter as tk
from ui.interfejs_fiszki import FlashcardInterface

# Tryb nauki - losowe fiszki do momentu wyjścia

def run(flashcards, mode):
    used_indices = set()

    def show_random_flashcard():
        if len(used_indices) == len(flashcards):
            print("Wszystkie fiszki zostały pokazane.")
            return

        index = random.choice([i for i in range(len(flashcards)) if i not in used_indices])
        used_indices.add(index)

        def on_quit():
            print("Wyjście z trybu nauki")

        def go_next():
            app.root.destroy()
            show_random_flashcard()

        dummy = lambda: None

        app = FlashcardInterface(
            json_path=None,  # Nie wczytujemy z pliku
            index=0,
            callbacks={
                'quit': on_quit,
                'next': go_next,
                'prev': dummy,
                'toggle': dummy,
                'yes': go_next,   # ← TERAZ 'Y' też działa jak 'N'
                'no': go_next,
            },
            mode=mode
        )

        # Ustaw okno jako "pełnoekranowe"
        app.root.attributes('-topmost', True)
        app.root.attributes('-fullscreen', True)  # ← ta linia została dodana
        app.root.focus_force()
        app.root.lift()

        # Ręczne podstawienie fiszki i aktualizacja interfejsu
        app.set_card(flashcards[index])
        app.run()

    # Ukryj techniczne okno inicjalne Tkintera
    dummy_root = tk.Tk()
    dummy_root.withdraw()
    show_random_flashcard()
