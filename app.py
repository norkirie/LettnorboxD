import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
from movie import Movie
from watchlist import Watchlist

class WatchlistApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LettnorboxD")
        self.watchlist = Watchlist()
        
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        self.root.geometry("1000x600")
    
        self.setup_ui()

    def setup_ui(self):

        frame_add = ctk.CTkFrame(self.root)
        frame_add.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(frame_add, text="Title:", font=("lato", 15, "bold")).grid(row=0, column=0, padx=5, pady=5)
        self.entry_title = ctk.CTkEntry(frame_add)
        self.entry_title.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(frame_add, text="Genre:", font=("lato", 15, "bold")).grid(row=1, column=0, padx=5, pady=5)
        self.entry_genre = ctk.CTkEntry(frame_add)
        self.entry_genre.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(frame_add, text="Year:", font=("lato", 15, "bold")).grid(row=2, column=0, padx=5, pady=5)
        self.entry_year = ctk.CTkEntry(frame_add)
        self.entry_year.grid(row=2, column=1, padx=5, pady=5)

        ctk.CTkLabel(frame_add, text="Rating:", font=("lato", 15, "bold")).grid(row=3, column=0, padx=5, pady=5)
        self.entry_rating = ctk.CTkEntry(frame_add)
        self.entry_rating.grid(row=3, column=1, padx=5, pady=5)

        ctk.CTkLabel(frame_add, text="Comments:", font=("lato", 15, "bold")).grid(row=4, column=0, padx=5, pady=5)
        self.entry_comments = ctk.CTkEntry(frame_add)
        self.entry_comments.grid(row=4, column=1, padx=5, pady=5)

        self.button_add = ctk.CTkButton(frame_add, text="Add Movie", font=("lato", 15, "bold"), command=self.add_movie)
        self.button_add.grid(row=5, column=0, columnspan=2, pady=10)

        frame_view = ctk.CTkFrame(self.root)
        frame_view.pack(pady=10, padx=10, fill="both", expand=True)

        columns = ("ID", "Title", "Genre", "Year", "Rating", "Comments")
        self.tree = ttk.Treeview(frame_view, columns=columns, show="headings")

        self.tree.configure(style="Treeview")
        self.tree.pack(fill="both", expand=True)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        self.tree.pack(fill="both", expand=True)

        frame_buttons = ctk.CTkFrame(self.root)
        frame_buttons.pack(pady=10, padx=10, fill="x")

        self.button_update = ctk.CTkButton(frame_buttons, text="Update Movie", font=("lato", 15, "bold"), command=self.update_movie)
        self.button_update.grid(row=0, column=0, padx=5)

        self.button_delete = ctk.CTkButton(frame_buttons, text="Delete Movie", font=("lato", 15, "bold"), command=self.delete_movie)
        self.button_delete.grid(row=0, column=1, padx=5)

        self.button_import = ctk.CTkButton(frame_buttons, text="Import CSV", font=("lato", 15, "bold"), command=self.import_csv)
        self.button_import.grid(row=0, column=2, padx=5)

        self.button_export = ctk.CTkButton(frame_buttons, text="Export CSV", font=("lato", 15, "bold"), command=self.export_csv)
        self.button_export.grid(row=0, column=3, padx=5)

        self.refresh_treeview()

    def add_movie(self):
        title = self.entry_title.get()
        genre = self.entry_genre.get()
        year = self.entry_year.get()
        rating = self.entry_rating.get()
        comments = self.entry_comments.get()

        if not title or not genre or not year or not rating:
            messagebox.showerror("Error", "All fields except comments are required!")
            return

        try:
            year = int(year) 
            rating = float(rating)  
                
            if rating < 1 or rating > 5:
                messagebox.showerror("Error", "Rating must be between 1 and 5.")
                return

        except ValueError:
            messagebox.showerror("Error", "Year must be an integer and rating must be a number.")
            return

        movie = Movie(title=title, genre=genre, year=year, rating=rating, comments=comments)
        self.watchlist.add_movie(movie)
        self.refresh_treeview()
        self.clear_entries()

    def update_movie(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No movie selected.")
            return

        movie_id = int(self.tree.item(selected_item, "values")[0])
        for movie in self.watchlist.view_movies():
            if movie.movie_id == movie_id:
                movie.title = self.entry_title.get()
                movie.genre = self.entry_genre.get()
                try:
                    movie.year = int(self.entry_year.get())
                    movie.rating = float(self.entry_rating.get())
                except ValueError:
                    messagebox.showerror("Error", "Year must be an integer and rating must be a number.")
                    return
                movie.comments = self.entry_comments.get()
                self.watchlist.update_movie(movie)
                break

        self.refresh_treeview()

    def delete_movie(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No movie selected.")
            return

        movie_id = int(self.tree.item(selected_item, "values")[0])
        self.watchlist.delete_movie(movie_id)
        self.refresh_treeview()

    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.watchlist.load_from_csv(file_path)
            self.refresh_treeview()

    def export_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.watchlist.save_to_csv(file_path)

    def refresh_treeview(self):
        self.tree.delete(*self.tree.get_children())
        for movie in self.watchlist.view_movies():
            self.tree.insert("", "end", values=(
                movie.movie_id, movie.title, movie.genre, movie.year, movie.rating, movie.comments
            ))

    def clear_entries(self):
        self.entry_title.delete(0, "end")
        self.entry_genre.delete(0, "end")
        self.entry_year.delete(0, "end")
        self.entry_rating.delete(0, "end")
        self.entry_comments.delete(0, "end")

if __name__ == "__main__":
    root = ctk.CTk() 
    app = WatchlistApp(root) 
    root.mainloop()



















