"""CSC111 Project 2 - Movie Recommendation System
Last Updated: 29/3/25
Edited by: Aiden
"""
from graph_building import *


class BackendInstance:
    """ Represents an instance of a backend for the recommendation app.

    This should be a singleton, although it is not enforced.

    Holds the review graph, and has functions necessary to generate data for the frontend.
    """
    _review_graph: ReviewGraph

    def __init__(self, titles_file: str, ratings_file: str) -> None:
        self._review_graph = ReviewGraph()

        movie_titles = load_movies_from_file(titles_file, self._review_graph)

        load_reviews_from_file(ratings_file, self._review_graph, movie_titles)

    def get_movies(self) -> list[str]:
        """Return a list of movies included in the dataset.
        """
        return self._review_graph.get_movies()

    def get_genres(self) -> list[str]:
        """Return a list of all genres represented in the dataset.
        """
        return self._review_graph.get_genres()

    def get_recs_from_genres(self, genres: list[str], num_recs: int) -> \
            list[tuple[str, int, float, set[str]]]:
        """Return a list of recommended movies based on the given genres.

        The tuples contained in the returned list hold a movie title, year of release, rating, & genre.
        """
        movies = self._review_graph.recommend_by_genre(genres, num_recs)

        return self._format_recommendations(movies)

    # TODO: TEST IF THIS ACTUALLY WORKS!!!
    def get_recs_from_movies(self, liked_movies: set[str], num_recs: int) -> \
            list[tuple[str, int, float, set[str]]]:
        """Return a list of recommended movies based on the given liked movies.

        The tuples contained in the returned list hold a movie title, year of release, rating, & genre.
        Preconditions:
        All liked movies should be vertexes in the graph with at least one review.
        """
        # If we want to have them customize a minimum rating, it should be added to this function
        movies = self._review_graph.recommend_by_similarity(liked_movies, num_recs)

        return self._format_recommendations(movies)

    def _format_recommendations(self, movies: list[str]) -> list[tuple[str, int, float, set[str]]]:
        """Return a list of tuples containing info corresponding to the movie in movies. 
        """
        detailed_movies = []

        for movie in movies:
            detailed_movies.append(self._review_graph.get_movie_details(movie))

        return detailed_movies


if __name__ == '__main__':
    # You can uncomment the following lines for code checking/debugging purposes.
    # However, we recommend commenting out these lines when working with the large
    # datasets, as checking representation invariants and preconditions greatly
    # increases the running time of the functions/methods.
    # import python_ta.contracts
    # python_ta.contracts.check_all_contracts()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['E1136'],
        'extra-imports': ['graph_building'],
        'max-nested-blocks': 4
    })
