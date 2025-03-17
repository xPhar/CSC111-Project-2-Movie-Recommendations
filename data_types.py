from __future__ import annotations
from typing import Any

# Note: These classes are currently taken directly from Exercise 3, they should be updated as we decide how our data will be layed out
# TODO: Figure out the above :)

class _Vertex:
    """A vertex superclass, holding fields and methods shared by both movies and users

    Instance Attributes:
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """
    neighbours: set[_Vertex]

    def __init__(self) -> None:
        """Initialize a new vertex with no neighbours.
        """
        self.neighbours = set()

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)


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
        super.__init__()

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
        super.__init__()

        self.user_id = user_id


class Review_Graph:
    """A graph used to represent a network of movie reviews.

    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    _vertices: dict[Any, _Vertex]

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

    # TODO: Update this to add review, which will involve figuring out how to hold onto review scores
    def add_edge(self, item1: Any, item2: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            raise ValueError

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            return False

    def get_neighbours(self, item: Any) -> set:
        """Return a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return {neighbour.item for neighbour in v.neighbours}
        else:
            raise ValueError

    def get_all_vertices(self, kind: str = '') -> set:
        """Return a set of all vertex items in this graph.

        If kind != '', only return the items of the given vertex kind.

        Preconditions:
            - kind in {'', 'user', 'movie'}
        """
        if kind != '':
            return {v.item for v in self._vertices.values() if v.kind == kind}
        else:
            return set(self._vertices.keys())
