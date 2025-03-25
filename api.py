from graph_building import *

class BackendInstance:
    """ Represents an instance of a backend for the recommendation app.

    This should be a singleton, although it is not enforced.

    Holds the review graph, and has functions necessary to generate data for the frontend.
    """
    review_graph: Review_Graph

    def __init__(self, titles_file: str, ratings_file: str) -> None:
        self.review_graph = Review_Graph()

        movie_titles = load_movies_from_file(titles_file, self.review_graph)

        load_reviews_from_file(ratings_file, self.review_graph, movie_titles)

    def get_movies(self) -> list[str]:
        """Return a list of movies included in the dataset.
        """
        return self.review_graph.get_reviewed_movies()

    def get_recommendations_from_genres(self, genres: list[str], num_recs: int) -> list[tuple[str, int, float, set[str]]]:
        """ Return a list of recommended movies based on the given genres.

        The tuples contained in the returned list holds a movie title, year of release, rating, and genre.
        """
        movies = self.review_graph.recommend_by_genre(genres, num_recs)

        return self._format_recommendations(movies)

    # TODO: TEST IF THIS ACTUALLY WORKS!!!
    def get_recommendations_from_movies(self, liked_movies: set[str], num_recs: int) -> list[tuple[str, int, float, set[str]]]:
        """

        Preconditions:
        All liked movies should be vertexes in the graph with at least one review.
        """
        # If we want to have them customize a minimum rating, it should be added to this function
        movies = self.review_graph.recommend_by_similarity(liked_movies, num_recs)

        return self._format_recommendations(movies)

    def _format_recommendations(self, movies: list[str]) -> list[tuple[str, int, float, set[str]]]:
        movie_objects = [self.review_graph._vertices[movie] for movie in movies]

        return [(movie.title, movie.year, movie.avg_review_score(), movie.genres) for movie in movie_objects]
