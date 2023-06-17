import sys
import random
import json
import requests
from operator import itemgetter

PLACEHOLDER_TITLE = "__TEMPLATE_TITLE__"
PLACEHOLDER_MOVIES = "__TEMPLATE_MOVIE_GRID__"
WEBSITE_TITLE = "MOVIES ON DEMAND"
URL = "http://www.omdbapi.com/?apikey=67fde472&"
IMDB_API = "https://imdb-api.com/en/API/SearchMovie/k_r2vt4jtu/"
IMDB_URL = "https://www.imdb.com/title/"


class MovieApp:
    def __init__(self, storage):
        self.storage = storage

    def _command_list_movies(self):
        movies = self.storage.list_movies()
        print("\n" + str(len(movies)) + " movies found in total\n")
        for name, details in movies.items():
            print(f'{name} : {str(details["rating"])}, year:{details["year"]}')
        input("\nPress enter to continue:")

    def _command_add_movie(self):
        movies = self.storage.list_movies()
        new_movie = str(input("\nEnter new movie name : "))
        if new_movie.casefold() in [movie.casefold() for movie in movies]:
            print(f'Movie {new_movie} is already listed\n')
            return
        movie_data = json.loads(requests.get(URL + "t=" + new_movie).text)
        if "Error" in movie_data:
            print(f'{movie_data["Error"]}')
            input("\nPress enter to continue:")
            return
        title = movie_data["Title"]
        rating = float(movie_data["Ratings"][0]["Value"].split("/")[0])
        year = movie_data["Year"]
        poster = movie_data["Poster"]
        res = json.loads(requests.get(IMDB_API + title).text)
        imdb_id = res["results"][0]["id"]
        imdb_link = IMDB_URL + imdb_id
        self.storage.add_movie(title, year, rating, poster, imdb_link)
        input("\nPress enter to continue:")

    def _command_delet_movie(self):
        movies = self.storage.list_movies()
        movie_to_delet = input("\nEnter movie name to delet: ")
        if movie_to_delet not in movies:
            print(f'Movie name {movie_to_delet} is not available to delet\n')
            input("\nPress enter to continue:")
            return
        self.storage.delete_movie(movie_to_delet)
        print(f"Movie : {movie_to_delet} deleted successfully")
        input("\nPress enter to continue:")

    def _command_update_movie(self):
        movies = self.storage.list_movies()
        movie_to_update = str(input("\nEnter movie name : "))
        if movie_to_update not in movies:
            print(f'Movie name {movie_to_update} is not available in movies list\n')
            return
        notes = str(input("\nEnter movie note : "))
        self.storage.update_movie(movie_to_update, notes)
        print("Movie note updated successfully")
        input("\nPress enter to continue:")

    def _command_movie_stats(self):
        movies = self.storage.list_movies()
        total_rating = 0
        movie_and_rating_tuples = []
        for details in movies.values():
            total_rating += int(details["rating"])
        for name, details in movies.items():
            movie_and_rating_tuples.append(tuple((name, details["rating"])))
        sorted_list_tuple = sorted(movie_and_rating_tuples, key=itemgetter(1), reverse=True)
        if len(sorted_list_tuple) % 2 != 0:
            median_position = int((len(sorted_list_tuple) - 1) / 2 + 1)
            median_rating = {sorted_list_tuple[median_position][1]}
        else:
            median_position_1 = int((len(sorted_list_tuple) / 2))
            median_position_2 = int((len(sorted_list_tuple) / 2) + 1)
            rating_1 = sorted_list_tuple[median_position_1 - 1][1]
            rating_2 = sorted_list_tuple[median_position_2 - 1][1]
            median_rating = int((rating_1 + rating_2) / 2)
        print(f'\nAverage rating is : {total_rating / len(movies.values())}')
        print(f'\nMedian rating is : {median_rating}')
        print(f'\nBest movie: {sorted_list_tuple[0][0]} , Rating : {sorted_list_tuple[0][1]}\n')
        print(f'Worst movie: {sorted_list_tuple[-1][0]} , Rating : {sorted_list_tuple[-1][1]}')
        input("\nPress enter to continue:")

    def _command_random_movie(self):
        movies = self.storage.list_movies()
        movie_choice = random.choice(list(movies))
        ratting = movies[movie_choice]["rating"]
        print(f'\nYour movie for tonight: {movie_choice}, its rated : {ratting}')
        input("\nPress enter to continue:")

    def _command_search_movie(self):
        movies = self.storage.list_movies()
        search_str = str(input("\nEnter part of movie name: "))
        movie_list = list(movies)
        search_result = []
        for movie in movie_list:
            if search_str.casefold() in movie.casefold():
                search_result.append(movie)
        if len(search_result) != 0:
            for movie in search_result:
                print(f'{movie}, Ratting : {movies[movie]["rating"]}')
        else:
            print(f'The movie "{search_str}" is not in the list')
        input("\nPress enter to continue:")

    def _command_sorted_movie_list(self):
        movies = self.storage.list_movies()
        print("\n See soretd movie list by rating below:\n")
        movie_and_rating_tuples = []
        for name, details in movies.items():
            movie_and_rating_tuples.append(tuple((name, details["rating"])))
        sorted_list_tuple = sorted(movie_and_rating_tuples, key=itemgetter(1), reverse=True)
        for name, rating in sorted_list_tuple:
            print(f"{name} : {rating}")
        input("\nPress enter to continue:")

    def _command_generate_website(self):
        movies = self.storage.list_movies()
        output = ""
        for single_movie in movies:
            output += '<li>'
            output += ""
            output += f'<a href="{movies[single_movie]["IMDB_link"]}"><img class="movie-poster" ' \
                      f'src="{movies[single_movie]["poster"]}"></a>'
            output += f'<div class="movie-title">{single_movie}</div>'
            output += f'<div class="movie-year">{movies[single_movie]["year"]}</div>'
            output += f'<div class="movie-rating">{movies[single_movie]["rating"]}</div>'
            output += '</li>'
        with open("_static/index_template.html", "r") as fileobj:
            data = fileobj.read()
        with open("_static/website.html", "w") as fileobj:
            updated_text = data.replace(PLACEHOLDER_TITLE, WEBSITE_TITLE).replace(PLACEHOLDER_MOVIES, output)
            fileobj.write(updated_text)
        print("Website Generated successfully")
        input("\nPress enter to continue:")

    def _command_exit(self):
        sys.exit("Bye!")

    def run(self):
        while True:
            try:
                print("""********** My Movies Database ********** \n\n Menu: \n\n0. Exit \n1. List movies \n2. Add movie 
3. Delete movie \n4. Update movie \n5. Stats \n6. Random movie \n7. Search movie 
8. Movies sorted by rating \n9. Generate Website""")
                user_input = int(input("\nEnter choice (1-8) : "))
            except:
                print("\nInvalid Input\n")
                continue
            if user_input == 1:  # For list out movies
                self._command_list_movies()
            elif user_input == 2:  # For New Movie
                self._command_add_movie()
            elif user_input == 3:  # For Deleting movie
                self._command_delet_movie()
            elif user_input == 4:  # For Updating movie
                self._command_update_movie()
            elif user_input == 5:  # Displaying statistics
                self._command_movie_stats()
            elif user_input == 6:  # If user want Random Movie
                self._command_random_movie()
            elif user_input == 7:  # Search Movie
                self._command_search_movie()
            elif user_input == 8:  # For sorted movie list
                self._command_sorted_movie_list()
            elif user_input == 9:
                self._command_generate_website()
            elif user_input == 0:
                self._command_exit()
