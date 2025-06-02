import os
import json
#from logic import mode_learning, mode_test, mode_review
from logic import mode_learning, mode_test

# Mapowanie poziomow na pliki JSON
LEVEL_TO_FILE = {
    "B2": "data/fiszki_B2_unikalne.json",
    "C1": "data/fiszki_C1_unikalne.json",
    "C2": "data/fiszki_C2_unikalne.json",
}

def run_pipeline(level, mode, typ):
    json_path = LEVEL_TO_FILE.get(level)

    print(f"[DEBUG] level = '{level}'")
    print(f"[DEBUG] json_path = '{json_path}'")
    print(f"[DEBUG] exists = {os.path.exists(json_path)}")

    if not json_path or not os.path.exists(json_path):
        print(f"Błąd: nie znaleziono pliku JSON dla poziomu {level}.")
        return

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Błąd wczytywania pliku: {e}")
        return

    # Obsługa struktury danych
    if isinstance(data, dict):
        flashcards = []
        for group in data.values():
            flashcards.extend(group)
    elif isinstance(data, list):
        flashcards = data
    else:
        print("Nieprawidłowy format danych JSON")
        return

    # Routing do odpowiedniego trybu
    if typ == "nauka":
        mode_learning.run(flashcards, mode)
    elif typ == "sprawdzian":
        mode_test.run(flashcards, mode)
    #elif typ == "powtórka":
    #    mode_review.run(flashcards, mode)
    else:
        print(f"Nieznany tryb: {typ}")
