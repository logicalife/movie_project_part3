from istorage import IStorage


class StorageCsv(IStorage):
    def __init__(self,storage_path):
        self.filepath = storage_path

    def list_movies(self):
        pass

    def add_movie(self, title, year, rating, poster, imdb_link):
        pass

    def delete_movie(self, title):
        pass

    def update_movie(self, title, notes):
        pass



