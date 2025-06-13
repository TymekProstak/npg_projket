import random
import tkinter as tk
from ui.interfejs_fiszki import FlashcardInterface
import json

# Tryb sprawdzianu - każda fiszka raz, wynik na końcu
def run(flashcards, mode, json_path):
    random.shuffle(flashcards)
    index = 0
    correct_count = 0
    history = []  # Historia wyświetlanych fiszek

    app = FlashcardInterface(
        json_path=None,
        index=0,
        callbacks={
            'quit': lambda: app.root.destroy(),
            'next': lambda: next_card(),
            'prev': lambda: prev_card(),
            'toggle': lambda: None,
            'yes': lambda: mark_correct(),
            'no': lambda: mark_unknown(),
        },
        mode=mode
    )

    def next_card():
        nonlocal index
        if index < len(flashcards) - 1:
            history.append(index)
            index += 1
            app.set_card(flashcards[index])
        else:
            show_result()

    def prev_card():
        nonlocal index
        if history:
            index = history.pop()
            app.set_card(flashcards[index])
        else:
            print("Nie można cofnąć się dalej.")

    def mark_correct():
        nonlocal correct_count
        correct_count += 1
        next_card()

    def mark_unknown():
        flashcards[index]["nieznane"] += 1  # Zwiększ "nieznane"
        print(f"Zwiększono 'nieznane' dla fiszki: {flashcards[index]}")  # Debug
        save_flashcards()
        next_card()

    def save_flashcards():
        print("save_flashcards wywołane")  # Debug
        # Wczytaj wszystkie fiszki z pliku JSON
        with open(json_path, "r", encoding="utf-8") as f:
            all_flashcards = json.load(f)

        # Aktualizuj tylko bieżącą fiszkę
        current_card = flashcards[index]
        for original_card in all_flashcards:
            if current_card.get("polski") == original_card.get("polski") and current_card.get("angielski") == original_card.get("angielski"):
                print(f"Aktualizuję fiszkę: {current_card}")  # Debug
                original_card["nieznane"] = current_card["nieznane"]

        # Zapisz zaktualizowane fiszki do pliku JSON
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(all_flashcards, f, ensure_ascii=False, indent=4)
            print(f"Zapisano zmiany do pliku: {json_path}")  # Debug

    def show_result():
        app.root.destroy()
        print(f"Test zakończony. Wynik: {correct_count}/{len(flashcards)}")

    app.set_card(flashcards[index])
    app.run()
