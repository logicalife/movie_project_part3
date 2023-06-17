from movie_app import MovieApp
from storage_json import StorageJson
from storage_csv import StorageCsv


def main():
    storage1 = StorageJson("movies.json")
    movie_app1 = MovieApp(storage1)
    storage2 = StorageCsv("movies.csv")
    movie_app2 = MovieApp(storage2)

    movie_app2.run()


if __name__ == "__main__":
    main()
