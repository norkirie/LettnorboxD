import customtkinter as ctk
from app import Watchlist 

def main():
    root = ctk.CTk()
    app = Watchlist(root)
    root.mainloop()

if __name__ == "__main__":
    main()


