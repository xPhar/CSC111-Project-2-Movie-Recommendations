"""CSC111 Project 2 - Movie Recommendation System
Last Updated: 29/3/25
Edited by: Aiden
"""
import pandas as pd
from data_types import *


def load_movies_from_file(file_path: str, graph: ReviewGraph) -> dict[int, str]:
    """Return a dictionary mapping movie id's to the corresponding title in the dataset.

    Preconditions:
    - file_path corresponds to a csv file from the MovieLens dataset mapping movie id's to titles.
    """
    dataframe = pd.read_csv(file_path, dtype={"movieId": "int32", "title": "str", "genres": "str"})

    movie_names = {}

    for row in dataframe.itertuples(index=False):
        # Strip year from the end of the title
        # This assumes that all movies have a four-digit year of release :D
        title, year = row.title[:len(row.title) - 6].strip(), row.title[len(row.title) - 6:]

        movie_names[row.movieId] = title
        graph.add_movie(title, year, set(row.genres.split("|")))

    return movie_names


def load_reviews_from_file(file_path: str, graph: ReviewGraph, movies: dict[int, str]) -> None:
    """Fill the given graph with movie and user verticies connected by reviews from the dataset.

    Preconditions:
    - file_path corresponds to a csv file from the MovieLens dataset mapping users to movies w/ review scores.
    """
    dataframe = pd.read_csv(file_path,
                            usecols={"userId", "movieId", "rating"},
                            dtype={"userId": "int32", "movieId": "int32", "rating": "float32"})

    for row in dataframe.itertuples(index=False):
        graph.add_user(row.userId)

        graph.add_review(row.userId, movies[row.movieId], row.rating)


if __name__ == '__main__':
    # You can uncomment the following lines for code checking/debugging purposes.
    # However, we recommend commenting out these lines when working with the large
    # datasets, as checking representation invariants and preconditions greatly
    # increases the running time of the functions/methods.
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['data_types, pandas']
    })
