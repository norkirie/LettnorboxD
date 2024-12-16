import customtkinter as ctk
from app import WatchlistApp

def main():
    root = ctk.CTk()
    app = WatchlistApp(root) 
    root.mainloop()

if __name__ == "__main__":
    main()


