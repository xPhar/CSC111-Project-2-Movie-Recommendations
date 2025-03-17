from data_types import *
import pandas as pd

def load_movies_from_file(file_path: str, graph: Review_Graph) -> dict[int, str]:
    # Note: nrows should be removed when trying to use the entire dataset
    dataframe = pd.read_csv(file_path, nrows=10, dtype={"movieId": "int32", "title": "str", "genres": "str"})

    movie_names = {}

    for row in dataframe.itertuples(index=False):
        # Strip year from the end of the title
        # This assumes that all movies have a four-digit year of release :D
        title, year = row.title[:len(row.title) - 6], row.title[len(row.title) - 6:]

        movie_names[row.movieId] = title
        graph.add_movie(title, year, {genre for genre in row.genres.split("|")})

    return movie_names

if __name__ == "__main__":
    graph = Review_Graph()

    movies = load_movies_from_file("data/ml-latest-small/movies.csv", graph)

    import pprint

    pprint.pprint(movies)