from movie_app import MovieApp
from storage_json import StorageJson


def main():
    storage1 = StorageJson("movies.json")
    movie_app1 = MovieApp(storage1)
    movie_app1.run()


if __name__ == "__main__":
    main()
