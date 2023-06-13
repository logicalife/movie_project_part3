from istorage import IStorage

class StorageJson(IStorage):
    def __init__(self,filepath):
        self.filepath = filepath
        movies =


    def list_movies(self):
        movies = movie_storage.get_list_movies()

    def add_movie(self,title,year,rating,poster):
        pass

    def delete_movie(self,title):
        pass

    def update_movie(self,title,notes):
        pass

