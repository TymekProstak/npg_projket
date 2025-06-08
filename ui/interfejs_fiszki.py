import json
import tkinter as tk
from tkinter import messagebox


class FlashcardInterface:
    def __init__(self, json_path, index, callbacks, mode):
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
        """
        # Wczytanie fiszek lub placeholder jeśli json_path is None
        if json_path is None:
            self.card = {"polski": "", "angielski": ""}
        else:
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
        self.mode = mode

        # Inicjalizacja okna
        self.root = tk.Tk()
        self.root.title("Flashcard Viewer")
        self.root.geometry("800x600")  # Fixed window size
        self.root.configure(bg="#f5f5f5")
        self.root.bind("<Key>", self.on_key)

        # Główna ramka
        self.main_frame = tk.Frame(self.root, bg="#ffffff", relief="groove", bd=2)
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Lewa strzałka do nawigacji
        self.left_arrow = tk.Label(
            self.main_frame,
            text="←",
            font=("Arial", 36, "bold"),
            bg="#ffffff",
            fg="#007acc",
        )
        self.left_arrow.place(relx=0.02, rely=0.5, anchor="w")  # Wyrównanie do lewej krawędzi

        # Etykieta polskiego słowa
        self.pol_label = tk.Label(
            self.main_frame,
            text="Polskie słowo",
            font=("Arial", 28, "bold"),
            wraplength=700,
            bg="#ffffff",
            fg="#333333",
        )
        self.pol_label.pack(expand=True, pady=(50, 40))  # Zwiększone odstępy poniżej polskiego słowa

        # Etykieta angielskiego słowa
        self.eng_label = tk.Label(
            self.main_frame,
            text="Angielskie tłumaczenie",
            font=("Arial", 24, "italic"),
            wraplength=700,
            bg="#ffffff",
            fg="#007acc",
        )
        self.eng_label.pack(expand=True, pady=(0, 50))  # Zwiększone odstępy powyżej angielskiego słowa

        # Prawa strzałka do nawigacji
        self.right_arrow = tk.Label(
            self.main_frame,
            text="→",
            font=("Arial", 36, "bold"),
            bg="#ffffff",
            fg="#007acc",
        )
        self.right_arrow.place(relx=0.98, rely=0.5, anchor="e")  # Wyrównanie do prawej krawędzi

        # Instrukcja na dole
        self.instr_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.instr_frame.pack(side="bottom", fill="x", pady=15)

        self.instr_text = tk.Text(
            self.instr_frame,
            font=("Arial", 16),  # Dostosowana wielkość czcionki
            fg="#333333",
            bg="#f5f5f5",
            height=4,  # Zachowaj tę samą wysokość
            bd=0,
            wrap="word",
        )
        self.instr_text.pack(expand=False, fill="x", padx=20, pady=10)

        # Zastosuj pogrubioną czcionkę do nazw klawiszy
        self.instr_text.tag_configure("bold", font=("Arial", 16, "bold"))
        self.instr_text.tag_configure("center", justify="center")  # Wyśrodkowanie
        self.instr_text.insert("end", "Spacja", ("bold", "center"))
        self.instr_text.insert("end", ": Obrót  ")
        self.instr_text.insert("end", "Y", ("bold", "center"))
        self.instr_text.insert("end", ": Znana  ")
        self.instr_text.insert("end", "N", ("bold", "center"))
        self.instr_text.insert("end", ": Nieznana  ")
        self.instr_text.insert("end", "Q", ("bold", "center"))
        self.instr_text.insert("end", ": Wyjdź")

        self.instr_text.tag_add("center", "1.0", "end")  # Wyśrodkowanie całego tekstu
        self.instr_text.configure(state="disabled")  # Ustawienie tekstu jako tylko do odczytu

        self.show_translation = False
        self.is_destroyed = False

    def on_key(self, event):
        print(f"Naciśnięto klawisz: {event.keysym}")  # Debug
        if event.keysym == "n":
            callback = self.callbacks.get("no", lambda: None)
            print(f"Wywołuję callback dla 'N': {callback}")  # Debug
            callback()
        elif self.is_destroyed:
            return

        if event.keysym == "q":
            self.is_destroyed = True
            self.root.destroy()
        elif event.keysym in ("right", "n"):
            self.callbacks.get("next", lambda: None)()
        elif event.keysym in ("left",):
            self.callbacks.get("prev", lambda: None)()
        elif event.keysym == "space":
            self.toggle_translation()
        elif event.keysym == "y":
            self.callbacks.get("yes", lambda: None)()
        elif event.keysym == "n":
            self.callbacks.get("no", lambda: None)()

    def toggle_translation(self):
        """Przełącz między wyświetlaniem a ukrywaniem angielskiego tłumaczenia."""
        if not self.show_translation:
            self.eng_label.config(text=self.card["angielski"])  # Pokaż rzeczywiste tłumaczenie
            self.show_translation = True
        else:
            self.eng_label.config(text="")  # Ukryj tłumaczenie
            self.show_translation = False

    def set_card(self, card):
        """Zaktualizuj zawartość bieżącej fiszki."""
        self.card = card
        self.pol_label.config(text=self.card["polski"])
        self.eng_label.config(text="")
        self.show_translation = False

    def run(self):
        self.root.mainloop()
