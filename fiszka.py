import json
import os
from status import StatusManager

class FlashcardManager:
    def __init__(self, json_path, status_path="status.json", mode='pl-en'):
        self.json_path = json_path
        self.status_manager = StatusManager(status_path)
        self.mode = mode
        self.index = 0
        self.level_name = os.path.basename(json_path).replace('.json', '')
        self.flashcards = self.load_flashcards()

    def load_flashcards(self):
        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, dict):
            flat = []
            for level in data.values():
                flat.extend(level)
            return flat
        elif isinstance(data, list):
            return data
        else:
            raise ValueError("Nieprawidłowy format JSON")

    def get_current_card(self):
        if 0 <= self.index < len(self.flashcards):
            return self.flashcards[self.index]
        return None

    def next_card(self):
        self.index = (self.index + 1) % len(self.flashcards)

    def prev_card(self):
        self.index = (self.index - 1) % len(self.flashcards)

    def get_front_text(self):
        card = self.get_current_card()
        return card["polski"] if self.mode == 'pl-en' else card["angielski"]

    def get_back_text(self):
        card = self.get_current_card()
        return card["angielski"] if self.mode == 'pl-en' else card["polski"]

    def set_mode(self, mode):
        if mode in ('pl-en', 'en-pl'):
            self.mode = mode

    def get_card_key(self, card=None):
        if card is None:
            card = self.get_current_card()
        if card is None:
            return None
        return f"{self.level_name}:{card['polski']}→{card['angielski']}"

    def mark_known(self):
        key = self.get_card_key()
        if key:
            self.status_manager.set(key, "znam")

    def mark_unknown(self):
        key = self.get_card_key()
        if key:
            self.status_manager.set(key, "nie znam")

    def is_known(self):
        key = self.get_card_key()
        return self.status_manager.is_known(key)

    def is_unknown(self):
        key = self.get_card_key()
        return self.status_manager.is_unknown(key)
