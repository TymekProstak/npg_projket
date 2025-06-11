# NPG Projekt - Gra Edukacyjna z Fiszkami

## **Opis Gry**
NPG Projekt to gra edukacyjna, która pomaga w nauce języka angielskiego za pomocą fiszek. Gracz może korzystać z różnych trybów, takich jak nauka, sprawdzian i powtórka, aby efektywnie przyswajać nowe słownictwo. Gra umożliwia również dodawanie i usuwanie fiszek, co pozwala na dostosowanie bazy słówek do indywidualnych potrzeb.

---

## **Tryby Gry**
1. **Nauka**:
   - W tym trybie gracz losowo przegląda fiszki, ucząc się nowych słówek.
   - Można oznaczyć fiszkę jako "nieznaną" (`N`), co zwiększa jej wartość `"nieznane"`, aby była częściej powtarzana.

2. **Sprawdzian**:
   - Gracz odpowiada na każdą fiszkę tylko raz.
   - Na końcu wyświetlany jest wynik testu.

3. **Powtórka**:
   - Gracz przegląda fiszki, które mają najwyższą wartość `"nieznane"`.
   - Można oznaczyć fiszkę jako "znaną" (`Y`), co resetuje jej wartość `"nieznane"` do `0`, lub jako "nieznaną" (`N`), co zwiększa tę wartość.

4. **Dodawanie Fiszek**:
   - Umożliwia dodanie nowych fiszek do bazy danych dla wybranego poziomu trudności (`B2`, `C1`, `C2`).

5. **Usuwanie Fiszek**:
   - Umożliwia usunięcie istniejących fiszek z bazy danych.

---

##  **Struktura Plików i za co odpowiadają ?**

### **Pliki w folderze `data`**
- Przechowują dane fiszek w formacie JSON. Każda fiszka zawiera pola:
  - `"polski"` - Polskie słowo.
  - `"angielski"` - Angielskie tłumaczenie.
  - `"nieznane"` - Liczba wskazująca, ile razy fiszka została oznaczona jako "nieznana".

### **Pliki w folderze `logic`**
- `controller.py` - Zarządza przepływem między trybami gry na podstawie wyboru użytkownika.
- `mode_learning.py` - Obsługuje logikę trybu nauki, w tym losowanie fiszek i oznaczanie ich jako "nieznane".
- `mode_test.py` - Obsługuje logikę trybu sprawdzianu, w tym ocenianie odpowiedzi gracza.
- `mode_review.py` - Obsługuje logikę trybu powtórki, w tym sortowanie fiszek według wartości `"nieznane"`.

### **Pliki w folderze `ui`**
- `interfejs_fiszki.py` - Wyświetla fiszki i obsługuje interakcje użytkownika (np. klawisze `Y`, `N`, `Q`).
- `add_flashcard_window.py` - Umożliwia dodawanie nowych fiszek do plików JSON.
- `delete_flashcard_window.py` - Umożliwia usuwanie istniejących fiszek z plików JSON.
- `selection_window.py` - Wyświetla główne okno wyboru trybu gry.

### **Plik `main.py`**
- Uruchamia aplikację i obsługuje wybór trybu gry.

---

## **Biblioteki**
Projekt korzysta z następujących bibliotek:
1. **Standardowe biblioteki Pythona**:
   - `json` - Do obsługi plików JSON.
   - `random` - Do losowania fiszek.
   - `tkinter` - Do tworzenia interfejsu graficznego.

2. **Wersja Pythona**:
   - Projekt działa na Pythonie 3.8 lub nowszym.

---

## **Instalacja**
1. **Zainstaluj Python**:
   - Upewnij się, że masz zainstalowanego Pythona w wersji 3.8 lub nowszej. Możesz pobrać go z [python.org](https://www.python.org/).

2. **Uruchom aplikację**:
   - W terminalu przejdź do folderu projektu:
     ```bash
     cd /home/tymek/npg/npg_projket
     ```
   - Uruchom aplikację:
     ```bash
     python main.py
     ```

3. **Dodatkowe wymagania**:
   - Nie są wymagane dodatkowe biblioteki, ponieważ projekt korzysta wyłącznie z bibliotek standardowych Pythona.

---

## **Jak korzystać z aplikacji?**
1. Uruchom aplikację za pomocą polecenia [python main.py](http://_vscodecontentref_/0).
2. Wybierz tryb gry w głównym oknie.
3. Korzystaj z klawiszy:
   - `Y` - Oznacz fiszkę jako "znaną".
   - `N` - Oznacz fiszkę jako "nieznaną".
   - `Q` - Wyjdź z trybu.
4. Dodawaj lub usuwaj fiszki w odpowiednich trybach.

---

Miłej nauki i powodzenia w grze! 🎉
