import random
import tkinter as tk
from ui.interfejs_fiszki import FlashcardInterface

# Tryb sprawdzianu - każda fiszka raz, wynik na końcu

def run(flashcards, mode):
    random.shuffle(flashcards)
    index = 0
    correct_count = 0

    def show_next_card():
        nonlocal index, correct_count

        if index >= len(flashcards):
            show_result()
            return

        card = flashcards[index]

        def on_quit():
            print("Przerwano test")
            app.root.destroy()
            show_result()

        def on_yes():
            nonlocal correct_count
            correct_count += 1
            app.root.destroy()
            next_card()

        def on_no():
            app.root.destroy()
            next_card()

        def next_card():
            nonlocal index
            index += 1
            show_next_card()

        dummy = lambda: None

        app = FlashcardInterface(
            json_path=None,
            index=0,
            callbacks={
                'quit': on_quit,
                'next': dummy,
                'prev': dummy,
                'toggle': dummy,
                'yes': on_yes,
                'no': on_no,
            },
            mode=mode
        )

        app.set_card(card)
        app.root.attributes('-topmost', True)
        app.root.attributes('-fullscreen', True)  # ← ta linia została dodana

        app.root.focus_force()
        app.root.lift()
        app.run()

    def show_result():
        result_window = tk.Tk()
        result_window.title("Wynik testu")
        result_window.geometry("400x200")

        total = len(flashcards)
        percent = round(100 * correct_count / total) if total else 0
        summary = f"Poprawne odpowiedzi: {correct_count} / {total} ({percent}%)"

        tk.Label(result_window, text=summary, font=("Arial", 16)).pack(pady=30)
        tk.Button(result_window, text="Zamknij", command=result_window.destroy).pack(pady=10)
        result_window.mainloop()

    show_next_card()
