from ui.selection_window import SelectionWindow
from ui.add_flashcard_window import AddFlashcardWindow
from ui.delete_flashcard_window import DeleteFlashcardWindow
from logic.controller import run_pipeline

def main():
    def on_submit(level, mode, typ):
        print(f"on_submit wywołane z level={level}, mode={mode}, typ={typ}")  # Debug
        run_pipeline(level, mode, typ)

    def on_add_flashcard():
        app = AddFlashcardWindow()
        app.run()

    def on_delete_flashcard():
        app = DeleteFlashcardWindow()
        app.run()

    app = SelectionWindow(on_submit, on_add_flashcard, on_delete_flashcard)
    app.run()

if __name__ == "__main__":
    main()
