from data_types import *
import pandas as pd

def load_movies_from_file(file_path: str, graph: Graph) -> dict[int, str]:
    # Note: nrows should be removed when trying to use the entire dataset
    dataframe = pd.read_csv(file_path, nrows=10, dtype={"movieId": "int32", "title": "str", "genres": "str"})

    movie_names = {}

    for row in dataframe.itertuples(index=False):
        movie_names[row.movieId] = row.title

    return movie_names

if __name__ == "__main__":
    graph = Graph()

    movies = load_movies_from_file("data/ml-latest-small/movies.csv", graph)

    import pprint

    pprint.pprint(movies)