from istorage import IStorage
import csv
import re


class StorageCsv(IStorage):
    def __init__(self, storage_path):
        self.filepath = storage_path

    def list_movies(self):
        movie_dict = {}
        with open (self.filepath, "r") as fileobj:
            csv_obj = csv.reader(fileobj)
            for row in csv_obj:
                if row:
                    movie_dict[row[0]] = dict({"year": row[1], "rating": float(row[2]), "poster": row[3], "IMDB_link": row[4]})
        return movie_dict

    def add_movie(self, title, year, rating, poster, imdb_link):
        new_movie_line = [title, year, rating, poster, imdb_link]
        with open(self.filepath, "a", newline='') as fileobj:
            csv_obj = csv.writer(fileobj)
            csv_obj.writerow(new_movie_line)
        return

    def delete_movie(self, title):
        with open(self.filepath, "r") as fileobj_to_read:
            csv_obj_r = csv.reader(fileobj_to_read)
            output = [x for x in csv_obj_r if x[0] != title]
        with open(self.filepath, "w") as fileobj_to_write:
            csv_obj_w = csv.writer(fileobj_to_write)
            for row in output:
                if row:
                    csv_obj_w.writerow(row)

    def update_movie(self, title, notes):
        with open(self.filepath, "r") as fileobj_to_read:
            csv_obj_r = csv.reader(fileobj_to_read)
            output = [x for x in csv_obj_r if len(x)>0]
        with open(self.filepath, "w") as fileobj_to_write:
            csv_obj_w = csv.writer(fileobj_to_write)
            for row in output:
                if row[0] == title:
                    if len(row) == 6:
                        row[5] = f"Note:{notes}"
                    row.append(f"Note:{notes}")
                if row:
                    csv_obj_w.writerow(row)
