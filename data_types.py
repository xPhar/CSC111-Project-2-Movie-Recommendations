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
    _reviews: set[Review]

    def __init__(self) -> None:
        """Initialize a new vertex with no reviews.
        """
        self._reviews = set()

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self._reviews)


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

    def avg_review_score(self) -> float:
        tot_rating = 0
        
        for review in self._reviews:
            tot_rating += review.rating

        return tot_rating / len(self._reviews)

    def bayesian_weighted_score(self, avg: float, num_confident: int) -> float:
        """ Return the weighted score of this movie.

        The weighted score will be from [0-5], calculated using the average review score,
        but taking into account the total number of reviews.

        For instance, a movie rated 5.0, but with only 1 or 2 reivews should be weighted lower
        than a movie with 10+ reviews. 
        """
        num_reviews = len(self._reviews)

        temp = num_reviews / (num_reviews + num_confident) * self.avg_review_score() \
                + num_confident / (num_reviews + num_confident) * avg

        return temp

    def similarity_score(self, other_movie: _Movie) -> float:
        """Return the similarity score between this movie and the other.
        """
        # A vertex has a similarity score of 0 to itself
        if self is other_movie:
            return 0

        # Create a set holding the verticies' shared neighbours
        shared_reviews = self._reviews.intersection(other_movie._reviews)
        # Create a set holding the verticies' non-shared neighbours
        unique_reviews = self._reviews.union(other_movie._reviews)
        # Return the number of shared neighbours / number of unique neighbours
        return len(shared_reviews) / len(unique_reviews)


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

            user._reviews.add(review)
            movie._reviews.add(review)
        else:
            raise ValueError

    def adjacent(self, user_id: int, movie_title: str) -> bool:
        """Return whether the user has reviewed the given movie.

        Return False if user_id or movie_title do not appear as vertices in this graph.
        """
        if user_id in self._vertices and movie_title in self._vertices:
            user = self._vertices[user_id]
            movie = self._vertices[movie_title]
            return any(movie is review.movie for review in user._reviews)
        else:
            return False
        
    def get_similarity_score(self, movie1: str, movie2: str) -> float:
        """Return the similarity score between the two given movies in this graph.

        Raise a ValueError if movie1 or movie2 do not appear as vertices in this graph.
        """
        # Check whether both items are verticies in this graph
        if movie1 in self._vertices and movie2 in self._vertices:
            # Get the associated verticies
            m1 = self._vertices[movie1]
            m2 = self._vertices[movie2]

            # Return the similarity between the two verticies
            # v2.similarity_score(v1) works identically
            return m1.similarity_score(m2)
        else:
            raise ValueError

    def get_movies(self) -> list[str]:
        return [vertex.title for vertex in self._vertices if type(vertex) is _Movie]
    
    def get_genres(self) -> list[str]:
        return {genre for genre in {self._vertices[movie].genres for movie in self.get_movies()}}

    def get_neighbours(self, item: int | str) -> set:
        """Return a set of the neighbours of the given item.

        If this is a user, return the titles of the movies they have reviewed.
        If this is a movie, return the user Id's of those which have reviewed it.
        """
        if item in self._vertices:
            vertex = self._vertices[item]
            if type(vertex) is _Movie:
                return {review.user.user_id for review in vertex._reviews}
            else:
                return {review.movie.title for review in vertex._reviews}
        else:
            raise ValueError

    def recommend_by_genre(self, genres: set[str], num_recommendations: int) -> list[str]:
        matching_movies = self._movies_matching_genre(genres)

        avg_movie_rating = self._avg_movie_rating()

        # This will sort from worst match to best, so we want the movies at the end of the list
        matching_movies.sort(key=lambda movie:_genre_recommendation_key(movie, genres, avg_movie_rating, 50))

        return [movie.title for movie in matching_movies[len(matching_movies) - num_recommendations:]]
        
    def _movies_matching_genre(self, genres: set[str]) -> list[_Movie]:
        return [vertex for vertex in self._vertices.values() if type(vertex) is _Movie and any({genre in vertex.genres for genre in genres}) and len(vertex._reviews) > 0] 

    def _avg_movie_rating(self) -> float:
        num_movies = 0
        total_score = 0
        for vertex in self._vertices.values():
            if type(vertex) is _Movie and len(vertex._reviews) > 0:
                num_movies += 1
                total_score += vertex.avg_review_score()
        
        return total_score / num_movies

    def recommend_by_similarity(self, movies: set[str], max_recommendations: int, min_rating: float = 3.5) -> list[str]:
        all_movies = self.get_movies()

        # Only look for movies with a weighted rating of at least min_rating
        movies_to_compare = [movie for movie in all_movies
                             if self._vertices[movie].bayesian_weighted_score(self._avg_movie_rating(), 50) > min_rating]
        
        similarity = self._calculate_similarities(movies, movies_to_compare)

        recommendations = [movie for movie in similarity.keys()].sort(key=lambda movie: similarity[movie])
        
        if len(recommendations) > max_recommendations:
            return recommendations[len(recommendations) - max_recommendations]
        else:
            return recommendations

    def _calculate_similarities(self, liked_movies: list[str], movies_to_compare: list[str]) -> dict[str, float]:
        net_similarity = {}
        
        for liked_movie in liked_movies:
            for movie in movies_to_compare:
                # Calculate the similarity score
                score = self.get_similarity_score(liked_movie, movie)

                # If the score is non-zero, add its score to the corresponding dictionary entry
                if score > 0:
                    if movie in net_similarity:
                        net_similarity[movie] += score
                    else:
                        net_similarity[movie] = score

        return net_similarity

def _genre_recommendation_key(movie: _Movie, genres: set[str], avg_rating: float, confidence_interval: int) -> float:
    weighted_score = movie.bayesian_weighted_score(avg_rating, confidence_interval)

    num_matching_genres = len(set(genres).intersection(movie.genres))
    num_genres = len(movie.genres)

    return weighted_score * (0.9 + (num_matching_genres / num_genres) / 10)
