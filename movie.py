class Movie:
    def __init__(self, title, genre, year, rating, comments, movie_id=None):
        self.title = title
        self.genre = genre
        self.year = year
        self.rating = rating
        self.comments = comments
        self.movie_id = movie_id

    def __repr__(self):
        return f"Movie({self.movie_id}, {self.title}, {self.year}, {self.rating}, {self.genre}, {self.comments})"


