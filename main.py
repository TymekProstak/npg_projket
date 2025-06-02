from ui.selection_window import SelectionWindow
from logic.controller import run_pipeline

def main():
    def on_submit(level, mode, typ):
        # Przekazuje wybór do kontrolera
        run_pipeline(level, mode, typ)

    app = SelectionWindow(on_submit)
    app.run()

if __name__ == "__main__":
    main()
