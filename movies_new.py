import sys
import random
import json
import requests
from storage_json import StorageJson
from operator import itemgetter

PLACEHOLDER_TITLE = "__TEMPLATE_TITLE__"
PLACEHOLDER_MOVIES = "__TEMPLATE_MOVIE_GRID__"
WEBSITE_TITLE = "MOVIES ON DEMAND"
URL = "http://www.omdbapi.com/?apikey=67fde472&"
IMDB_API = "https://imdb-api.com/en/API/SearchMovie/k_r2vt4jtu/"
IMDB_URL = "https://www.imdb.com/title/"

storage = StorageJson('movies.json')


def get_imdb_link(title):
    res = json.loads(requests.get(IMDB_API + title).text)
    imdb_id = res["results"][0]["id"]
    return IMDB_URL+imdb_id


def stats(movies):
    """This funstions provides statistics of the avialble movies"""
    total_rating = 0
    for details in movies.values():
      total_rating += int(details["rating"])
    print(f'\nAverage rating is : {total_rating/len(movies.values())}')
    movie_and_rating_tuples = []
    for name, details in movies.items():
        movie_and_rating_tuples.append(tuple((name,details["rating"])))
    sorted_list_tuple = sorted(movie_and_rating_tuples,key=itemgetter(1), reverse = True)
    if len(sorted_list_tuple) %2 != 0:
        median_position = int((len(sorted_list_tuple)-1)/2+1)
        median_rating = {sorted_list_tuple[median_position][1]}
    else:
        median_position_1 = int((len(sorted_list_tuple)/2))
        median_position_2 = int((len(sorted_list_tuple)/2)+1)
        rating_1 = sorted_list_tuple[median_position_1-1][1]
        rating_2 = sorted_list_tuple[median_position_2-1][1]
        median_rating = int((rating_1+rating_2) / 2)
    return sorted_list_tuple, median_rating


def search_movie(movies, search_str):
    """This function takes part of movie and searches in the list"""
    movie_list = list(movies)
    search_result = []
    for movie in movie_list:
        if search_str.casefold() in movie.casefold():
            search_result.append(movie)
    return search_result


def sort_movie(movies):
    """This functions sorts list of movie by higher ratings"""
    movie_and_rating_tuples = []
    for name,details in movies.items():
      movie_and_rating_tuples.append(tuple((name,details["rating"])))
    sorted_list_tuple = sorted(movie_and_rating_tuples,key=itemgetter(1), reverse = True)
    return sorted_list_tuple


def get_serialized_data(single_movie, movies):
    """Returns the serialized text for HTML code for single movie"""
    seriallized_text = ""
    seriallized_text += f'<a href="{movies[single_movie]["IMDB_link"]}"><img class="movie-poster" ' \
                        f'src="{movies[single_movie]["poster"]}"></a>'
    seriallized_text += f'<div class="movie-title">{single_movie}</div>'
    seriallized_text += f'<div class="movie-year">{movies[single_movie]["year"]}</div>'
    seriallized_text += f'<div class="movie-rating">{movies[single_movie]["rating"]}</div>'
    return seriallized_text


def generate_website(movies):
    """reads movie data and HTML template files and generates the HTML code for the website"""
    output = ""
    for each_movie in movies:
        output += '<li>'
        output += get_serialized_data(each_movie,movies)
        output += '</li>'
    with open("_static/index_template.html", "r") as fileobj:
        data = fileobj.read()
    with open("_static/website.html", "w") as fileobj:
        updated_text = data.replace(PLACEHOLDER_TITLE, WEBSITE_TITLE).replace(PLACEHOLDER_MOVIES, output)
        fileobj.write(updated_text)
    print("Website Generated successfully")


def main():
  """This function shows the main functions and asks for the user input for different tasks"""
  while True:
    try:
        print("""********** My Movies Database ********** \n\n Menu: \n\n0. Exit \n1. List movies 
2. Add movie \n3. Delete movie \n4. Update movie \n5. Stats \n6. Random movie \n7. Search movie 
8. Movies sorted by rating \n9. Generate Website""")
        user_input = int(input("\nEnter choice (1-8) : "))
    except:
        print("\nInvalid Input\n")
        continue
    movies = storage.list_movies()
    if user_input == 1:  # For list out movies
        print("\n" + str(len(movies)) + " movies found in total\n")
        for name, details in movies.items():
          print(f'{name} : {str(details["rating"])}, year:{details["year"]}')
        input("\nPress enter to continue:")
    elif user_input == 2:  # For New Movie
        new_movie = str(input("\nEnter new movie name : "))
        if new_movie.casefold() in [movie.casefold() for movie in movies]:
            print(f'Movie {new_movie} is already listed\n')
            continue
        movie_data = json.loads(requests.get(URL+ "t=" +new_movie).text)
        if "Error" in movie_data:
            print(f'{movie_data["Error"]}')
            input("\nPress enter to continue:")
            continue
        title = movie_data["Title"]
        rating = float(movie_data["Ratings"][0]["Value"].split("/")[0])
        year = movie_data["Year"]
        poster = movie_data["Poster"]
        imdb_link = get_imdb_link(title)
        storage.add_movie(title, year, rating, poster, imdb_link)
        input("\nPress enter to continue:")
    elif user_input == 3:  # For Deleting movie
        movie_to_delet = input("\nEnter movie name to delet: ")
        if movie_to_delet not in movies:
            print(f'Movie name {movie_to_delet} is not available to delet\n')
            continue
        storage.delete_movie(movie_to_delet)
        print(f"Movie : {movie_to_delet} deleted successfully")
        input("\nPress enter to continue:")
    elif user_input == 4:  # For Updating movie
        movie_to_update = str(input("\nEnter movie name : "))
        notes = str(input("\nEnter movie note : "))
        storage.update_movie(movie_to_update,notes)
        print("Movie note updated successfully")
        input("\nPress enter to continue:")
    elif user_input == 5:  # Displaying statistics
        sorted_list_tuple,median_rating = stats(movies)
        print(f'\nMedian rating is : {median_rating}')
        print(f'\nBest movie: {sorted_list_tuple[0][0]} , Rating : {sorted_list_tuple[0][1]}\n')
        print(f'Worst movie: {sorted_list_tuple[-1][0]} , Rating : {sorted_list_tuple[-1][1]}')
        input("\nPress enter to continue:")
    elif user_input == 6:  # If user want Random Movie
        movie_choice = random.choice(list(movies))
        ratting = movies[movie_choice]["rating"]
        print(f'\nYour movie for tonight: {movie_choice}, its rated : {ratting}')
        input("\nPress enter to continue:")
    elif user_input == 7:  # Search Movie
        search_str = str(input("\nEnter part of movie name: "))
        search_result = search_movie(movies, search_str)
        if len(search_result) != 0:
            for movie in search_result:
                print(f'{movie}, Ratting : {movies[movie]["rating"]}')
        else:
            print(f'The movie "{search_str}" is not in the list')
        input("\nPress enter to continue:")
    elif user_input == 8:  # For sorted movie list
        print("\n See soretd movie list by rating below:\n")
        sorted_tupple = sort_movie(movies)
        for name,rating in sorted_tupple:
            print(f"{name} : {rating}")
        input("\nPress enter to continue:")
    elif user_input == 9:
        generate_website(movies)
        input("\nPress enter to continue:")
    elif user_input == 0 :
        sys.exit("Bye!")


if __name__ == "__main__":
    main()

