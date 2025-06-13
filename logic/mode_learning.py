import random
import json
from ui.interfejs_fiszki import FlashcardInterface

# Tryb nauki - losowe fiszki do momentu wyjścia
def run(flashcards, mode, json_path):
    print(f"run wywołane z mode={mode}, json_path={json_path}")  # Debug
    used_indices = set()
    history = []  # Historia wyświetlanych fiszek
    index = None  # Bieżący indeks fiszki

    def show_random_flashcard():
        nonlocal index
        if len(used_indices) == len(flashcards):
            print("Wszystkie fiszki zostały pokazane.")
            return

        index = random.choice([i for i in range(len(flashcards)) if i not in used_indices])
        used_indices.add(index)
        history.append(index)
        print(f"Wyświetlam fiszkę: {flashcards[index]}")  # Debug
        app.set_card(flashcards[index])

    def go_next():
        show_random_flashcard()

    def go_prev():
        nonlocal index
        if len(history) > 1:
            history.pop()  # Usuń bieżący indeks z historii
            index = history[-1]  # Cofnij się do poprzedniego indeksu
            app.set_card(flashcards[index])
        else:
            print("Nie można cofnąć się dalej.")

    def on_quit():
        print("Wyjście z trybu nauki")
        app.root.destroy()

    def mark_unknown():
        print("mark_unknown wywołane")  # Debug
        current_card = app.card
        current_card["nieznane"] += 1
        save_flashcards()

    def save_flashcards():
        print("save_flashcards wywołane")  # Debug
        # Wczytaj wszystkie fiszki z pliku JSON
        with open(json_path, "r", encoding="utf-8") as f:
            all_flashcards = json.load(f)

        # Aktualizuj tylko bieżącą fiszkę
        current_card = app.card
        for original_card in all_flashcards:
            if current_card.get("polski") == original_card.get("polski") and current_card.get("angielski") == original_card.get("angielski"):
                print(f"Aktualizuję fiszkę: {current_card}")  # Debug
                original_card["nieznane"] = current_card["nieznane"]

        # Zapisz zaktualizowane fiszki do pliku JSON
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(all_flashcards, f, ensure_ascii=False, indent=4)
            print(f"Zapisano zmiany do pliku: {json_path}")  # Debug

    # Create a single instance of FlashcardInterface
    app = FlashcardInterface(
        json_path=None,  # Nie wczytujemy z pliku
        index=0,
        callbacks={
            'quit': on_quit,
            'next': go_next,
            'prev': go_prev,
            'toggle': lambda: None,
            'yes': go_next,
            'no': mark_unknown,  # Klawisz 'N' wywołuje mark_unknown
        },
        mode=mode
    )

    print(f"Przypisano funkcję mark_unknown do klawisza 'N': {mark_unknown}")

    # Show the first random flashcard
    show_random_flashcard()
    app.run()
