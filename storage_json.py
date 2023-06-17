from istorage import IStorage
import json

class StorageJson(IStorage):
    def __init__(self,filepath):
        self.filepath = filepath

    def list_movies(self):
        with open(self.filepath, "r") as fileobj:
            data = json.loads(fileobj.read())
        return data

    def add_movie(self, title, year, rating, poster,imdb_link):
        avlbl_movies = self.list_movies()
        avlbl_movies[title] = dict({"rating": rating, "year": year, "poster": poster, "IMDB_link": imdb_link})
        with open(self.filepath, "w") as fileobj:
            fileobj.write(json.dumps(avlbl_movies))

    def delete_movie(self, title):
        avlbl_movies = self.list_movies()
        del avlbl_movies[title]
        with open(self.filepath, "w") as fileobj:
            fileobj.write(json.dumps(avlbl_movies))

    def update_movie(self, title, notes_to_update):
        avlbl_movies = self.list_movies()
        if title not in avlbl_movies:
            print(f'Movie name {title} is not available in the list\n')
            return
        avlbl_movies[title]["notes"] = str(notes_to_update)
        with open(self.filepath, "w") as fileobj:
            fileobj.write(json.dumps(avlbl_movies))


