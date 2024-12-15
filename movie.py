class Movie:
    def __init__(self, title, genre, year, rating, comments, movieid):
        self.title = title
        self.genre = genre
        self.year = year
        self.rating = rating
        self.comments = comments
        self.movie_id = movieid


    def __repr__(self):
        return f"{self.title} ({self.year}) - {self.genre}"



