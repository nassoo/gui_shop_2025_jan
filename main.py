from canvas import app
from authentication import render_main_enter_screen

if __name__ == "__main__":
    render_main_enter_screen()
    app.mainloop()
    app.winfo_children()