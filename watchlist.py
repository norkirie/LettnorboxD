from movie import Movie
import csv

class Watchlist:
    def __init__(self):
        self.movies = []
        self.next_id = 1
        self.ratings = {}
        self.comments = {}

    def add_movie(self, movie):
        movie.movie_id = self.next_id
        self.movies.append(movie)
        self.next_id += 1

    def view_movies(self):
        return self.movies

    def update_movie(self, movie):
        for idx, m in enumerate(self.movies):
            if m.movie_id == movie.movie_id:
                self.movies[idx] = movie
                return

    def delete_movie(self, movie_id):
        self.movies = [movie for movie in self.movies if movie.movie_id != movie_id]

    def load_from_csv(self, file_name="movies.csv"):
        """Loads movie data from a single CSV file."""
        self.movies.clear()

        try:
            with open(file_name, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if len(row) < 6:
                        print(f"Skipping invalid row: {row}")
                        continue
                    
                    movie_id, title, genre, year, rating, comments = row
                    movie = Movie(
                        title=title,
                        genre=genre,
                        year=int(year),
                        rating=float(rating),
                        comments=comments,
                        movie_id=int(movie_id)
                    )
                    self.movies.append(movie)

                if self.movies:
                    self.next_id = max(movie.movie_id for movie in self.movies) + 1
                else:
                    self.next_id = 1

        except FileNotFoundError:
            print(f"{file_name} not found. Starting with an empty watchlist.")
        except Exception as e:
            print(f"Error loading data from CSV: {e}")

    def save_to_csv(self, file_name="movies.csv"):
        """Saves movie data to a single CSV file."""
        try:
            with open(file_name, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["movie_id", "title", "genre", "year", "ratings", "comments"])
                for movie in self.movies:
                    writer.writerow([
                        movie.movie_id,
                        movie.title,
                        movie.genre,
                        movie.year,
                        movie.rating,
                        movie.comments
                    ])
        except Exception as e:
            print(f"Error saving data to CSV: {e}")

