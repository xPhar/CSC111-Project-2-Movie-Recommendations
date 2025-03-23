from data_types import *
import pandas as pd

def load_movies_from_file(file_path: str, graph: Review_Graph) -> dict[int, str]:
    # Note: nrows should be removed when trying to use the entire dataset
    dataframe = pd.read_csv(file_path, dtype={"movieId": "int32", "title": "str", "genres": "str"})

    movie_names = {}

    for row in dataframe.itertuples(index=False):
        # Strip year from the end of the title
        # This assumes that all movies have a four-digit year of release :D
        title, year = row.title[:len(row.title) - 6].strip(), row.title[len(row.title) - 6:]

        movie_names[row.movieId] = title
        graph.add_movie(title, year, {genre for genre in row.genres.split("|")})

    return movie_names

def load_reviews_from_file(file_path: str, graph: Review_Graph, movies: dict[int, str]) -> None:
    dataframe = pd.read_csv(file_path,
                            usecols={"userId", "movieId", "rating"},
                            dtype={"userId": "int32", "movieId": "int32", "rating": "float32"})

    for row in dataframe.itertuples(index=False):
        graph.add_user(row.userId)

        graph.add_review(row.userId, movies[row.movieId], row.rating)

if __name__ == "__main__":
    graph = Review_Graph()

    movies = load_movies_from_file("data/ml-latest-small/movies.csv", graph)

    load_reviews_from_file("data/ml-latest-small/ratings.csv", graph, movies)

    cool_ones = graph.recommend_by_genre({"Comedy", "Romance"})

    import pprint

    pprint.pprint(cool_ones)
