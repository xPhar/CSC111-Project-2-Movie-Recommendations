from __future__ import annotations
from typing import Any

# Note: These classes are currently taken directly from Exercise 3, they should be updated as we decide how our data will be layed out
# TODO: Figure out the above :)

class _Vertex:
    """A vertex superclass, holding fields and methods shared by both movies and users

    Instance Attributes:
        - reviews: The reviews connecting this vertex to its neighbours.

    Representation Invariants:
        - self not in {review.user, review.movie for review in self.reviews}
    """
    reviews: set[Review]

    def __init__(self) -> None:
        """Initialize a new vertex with no reviews.
        """
        self.reviews = set()

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.reviews)


class _Movie(_Vertex):
    """A movie object, holding all information pertaining to a movie in the graph.

    Instance Attributes:
        - title: the title of the movie
        - year: the release year of the movie
        - genres: a set contianing the genres this movie fits into
    """
    title: str
    year: int
    genres: set[str]

    def __init__(self, title: str, year: int, genres: set[str]) -> None:
        """Initialize a new movie vertex with the given title, year, and genres.
        """
        super().__init__()

        self.title = title
        self.year = year
        self.genres = genres


class _User(_Vertex):
    """A user object, representing a user in the dataset who has made a review

    Instance Attributes:
        - user_id: the users unique id (from the dataset)
    """
    user_id: int

    def __init__(self, user_id: int) -> None:
        """Initialize a new user vertex with the given id.
        """
        super().__init__()

        self.user_id = user_id


class Review:
    """A review object, which acts as an edge in a Review Graph.

    Holds a user, a movie, and a rating (0 - 5).
    """
    user: _User
    movie: _Movie
    rating: float

    def __init__(self, user: _User, movie: _Movie, rating: float) -> None:
        self.user = user
        self.movie = movie
        self.rating = rating


class Review_Graph:
    """A graph used to represent a network of movie reviews.

    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    _vertices: dict[Any, _Movie | _User]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_movie(self, title: str, year: int, genres: set[str]) -> None:
        """Add a movie vertex with the given title, year, and genres to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given title is already in this graph.
        """
        if title not in self._vertices:
            self._vertices[title] = _Movie(title, year, genres)

    def add_user(self, user_id: int) -> None:
        """Add a user vertex with the given id to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given id is already in this graph.
        """
        if user_id not in self._vertices:
            self._vertices[user_id] = _User(user_id)

    def add_review(self, user_id: int, movie_title: str, score: int) -> None:
        """Add a review between the user and movie in this graph with the given score.

        Raise a ValueError if userid or title do not appear as vertices in this graph.
        """
        if user_id in self._vertices and movie_title in self._vertices:
            user = self._vertices[user_id]
            movie = self._vertices[movie_title]

            review = Review(user, movie, score)

            user.reviews.add(review)
            movie.reviews.add(review)
        else:
            raise ValueError

    def adjacent(self, user_id: int, movie_title: str) -> bool:
        """Return whether the user has reviewed the given movie.

        Return False if user_id or movie_title do not appear as vertices in this graph.
        """
        if user_id in self._vertices and movie_title in self._vertices:
            user = self._vertices[user_id]
            movie = self._vertices[movie_title]
            return any(movie is review.movie for review in user.reviews)
        else:
            return False

    def get_neighbours(self, item: int | str) -> set:
        """Return a set of the neighbours of the given item.

        If this is a user, return the titles of the movies they have reviewed.
        If this is a movie, return the user Id's of those which have reviewed it.
        """
        if item in self._vertices:
            vertex = self._vertices[item]
            if type(vertex) is _Movie:
                return {review.user.user_id for review in vertex.reviews}
            else:
                return {review.movie.title for review in vertex.reviews}
        else:
            raise ValueError

    def DEBUG_print_movies(self) -> None:
        for vertex in self._vertices.values():
            if type(vertex) is _Movie:
                print(vertex.title)

    def DEBUG_print_users(self) -> None:
        for vertex in self._vertices.values():
            if type(vertex) is _User:
                print(vertex.user_id)