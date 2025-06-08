import os
import json
from logic import mode_learning, mode_test, mode_review

# Mapowanie poziomow na pliki JSON
LEVEL_TO_FILE = {
    "B2": "data/fiszki_B2_unikalne.json",
    "C1": "data/fiszki_C1_unikalne.json",
    "C2": "data/fiszki_C2_unikalne.json",
}

def run_pipeline(level, mode, typ):
    print(f"run_pipeline wywołane z level={level}, mode={mode}, typ={typ}")  # Debug
    json_path = LEVEL_TO_FILE.get(level)
    if not json_path:
        print(f"[ERROR] Nie znaleziono pliku dla poziomu: {level}")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        flashcards = json.load(f)

    if typ == "powtórka":
        mode_review.run(flashcards, mode, json_path)
    elif typ == "nauka":
        mode_learning.run(flashcards, mode, json_path)
    elif typ == "sprawdzian":
        mode_test.run(flashcards, mode, json_path)
    else:
        print(f"[ERROR] Nieznany typ trybu: {typ}")
