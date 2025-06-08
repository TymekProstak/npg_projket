import random
from ui.interfejs_fiszki import FlashcardInterface
import json

def run(flashcards, mode, json_path):
    # Sortowanie fiszek według "nieznane" w kolejności malejącej i ograniczenie do 20
    flashcards = sorted(flashcards, key=lambda x: x["nieznane"], reverse=True)[:20]
    index = 0

    def next_card():
        nonlocal index
        if index < len(flashcards) - 1:
            index += 1
            app.set_card(flashcards[index])
        else:
            print("Powtórka zakończona.")
            app.root.destroy()

    def mark_known():
        flashcards[index]["nieznane"] = 0  # Reset "nieznane" to 0
        save_flashcards()
        next_card()

    def mark_unknown():
        flashcards[index]["nieznane"] += 1  # Increment "nieznane"
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

    app = FlashcardInterface(
        json_path=None,
        index=0,
        callbacks={
            'quit': lambda: app.root.destroy(),
            'next': lambda: next_card(),
            'prev': lambda: None,
            'toggle': lambda: None,
            'yes': lambda: mark_known(),
            'no': lambda: mark_unknown(),
        },
        mode=mode
    )

    app.set_card(flashcards[index])
    app.run()