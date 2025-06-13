import random
from ui.interfejs_fiszki import FlashcardInterface
import json

def run(flashcards, mode, json_path):
    flashcards = sorted(flashcards, key=lambda x: x["nieznane"], reverse=True)[:20]
    index = 0
    history = []  # Historia wyświetlanych fiszek

    def next_card():
        nonlocal index
        if index < len(flashcards) - 1:
            history.append(index)
            index += 1
            app.set_card(flashcards[index])
        else:
            print("Powtórka zakończona.")
            app.root.destroy()

    def prev_card():
        nonlocal index
        if history:
            index = history.pop()
            app.set_card(flashcards[index])
        else:
            print("Nie można cofnąć się dalej.")

    def mark_known():
        flashcards[index]["nieznane"] = 0
        save_flashcards()
        next_card()

    def mark_unknown():
        flashcards[index]["nieznane"] += 1
        save_flashcards()
        next_card()

    def save_flashcards():
        print("save_flashcards wywołane")  # Debug
        with open(json_path, "r", encoding="utf-8") as f:
            all_flashcards = json.load(f)

        current_card = flashcards[index]
        for original_card in all_flashcards:
            if current_card.get("polski") == original_card.get("polski") and current_card.get("angielski") == original_card.get("angielski"):
                print(f"Aktualizuję fiszkę: {current_card}")  # Debug
                original_card["nieznane"] = current_card["nieznane"]

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(all_flashcards, f, ensure_ascii=False, indent=4)
            print(f"Zapisano zmiany do pliku: {json_path}")  # Debug

    app = FlashcardInterface(
        json_path=None,
        index=0,
        callbacks={
            'quit': lambda: app.root.destroy(),
            'next': next_card,
            'prev': prev_card,
            'toggle': lambda: None,
            'yes': mark_known,
            'no': mark_unknown,
        },
        mode=mode
    )

    app.set_card(flashcards[index])
    app.run()