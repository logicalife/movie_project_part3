import random
import sys
from operator import itemgetter
import movie_storage
import requests
import json

PLACEHOLDER_TITLE = "__TEMPLATE_TITLE__"
PLACEHOLDER_MOVIES = "__TEMPLATE_MOVIE_GRID__"
WEBSITE_TITLE = "MOVIES ON DEMAND"
URL = "http://www.omdbapi.com/?apikey=67fde472&"



def main_menu_and_input():
  """Main menu and user input"""
  print("""********** My Movies Database ********** \n\n Menu: \n\n0. Exit \n1. List movies
2. Add movie \n3. Delete movie \n4. Update movie \n5. Stats \n6. Random movie
7. Search movie \n8. Movies sorted by rating \n9. Generate Website""")
  return int(input("\nEnter choice (1-8) : "))

def list_of_movies():
  """ This sfunction list outs avaialble list of movies with ratings"""
  movies = movie_storage.get_list_movies()
  print("\n" + str(len(movies)) + " movies found in total\n")
  for name,details in movies.items():
    print(f'{name} : {str(details["rating"])}, year:{details["year"]}')

def add_movie(new_movie):
  """This function adds a movie"""
  movies = movie_storage.get_list_movies()
  if new_movie.casefold() in [movie.casefold() for movie in movies]:
    print(f'Movie {new_movie} is already listed\n')
    return
  res = requests.get(URL+ "t=" +new_movie).text
  data = json.loads(res)
  if "Error" in data:
    print(f'{data["Error"]}')
    return
  title = data["Title"]
  rating = float(data["Ratings"][0]["Value"].split("/")[0])
  year = data["Year"]
  poster = data["Poster"]
  movie_storage.add_movie(title, rating, year, poster)
  return

def delet_movie(movie_to_delet):
  """This function takes asks for the movie name and delets if exists"""
  movies = movie_storage.get_list_movies()
  if movie_to_delet not in movies:
    print(f'Movie name {movie_to_delet} is not available to delet\n')
    return
  movie_storage.delete_movie(movie_to_delet)
  return True

def update_movie(movie_to_update):
  """This function asks for the movie name, if available it asks for the valid ratings to update"""
  movies = movie_storage.get_list_movies()
  if movie_to_update not in movies:
    print(f'Movie name {movie_to_update} is not available in the list\n')
    return
  else:
    updated_rating = float(input("Enter new movie rating (0-10): "))
    if updated_rating < 0 or updated_rating > 10:
      print(f'Rating {updated_rating} is invalid\n')
      return
    else:
      movie_storage.update_movie(movie_to_update, updated_rating)
      return


def random_movie():
  """This function chooses randim movies from avaialble list"""
  movies = movie_storage.get_list_movies()
  movie_choice = random.choice(list(movies))
  rat = movies[movie_choice]["rating"]
  return movie_choice,rat


def stats():
  """This funstions provides statistics of the avialble movies"""
  movies = movie_storage.get_list_movies()
  total_rating = 0
  for details in movies.values():
    total_rating = total_rating+ int(details["rating"])
  print(f'\nAverage rating is : {total_rating/len(movies.values())}')
  movie_and_rating_tuples = []
  for name,details in movies.items():
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
  return sorted_list_tuple,median_rating


def search_movie(search_str):
  """This function takes part of movie and searches in the list"""
  movies = movie_storage.get_list_movies()
  movie_list = list(movies.keys())
  search_result = []
  for movie in movie_list:
    if search_str.casefold() in movie.casefold():
      search_result.append(movie)
  if len(search_result) != 0:
    for movie in search_result:
      print(f'{movie}, Ratting : {movies[movie]["rating"]}')
  else:
      print(f'The movie "{search_str}" is not in the list')
  return


def sort_movie():
  """This functions sorts list of movie by higher ratings"""
  movies = movie_storage.get_list_movies()
  movie_and_rating_tuples = []
  for name,details in movies.items():
    movie_and_rating_tuples.append(tuple((name,details["rating"])))
  sorted_list_tuple = sorted(movie_and_rating_tuples,key=itemgetter(1), reverse = True)
  return sorted_list_tuple



def get_serialized_data(single_movie):
  """Returns the serialized text for HTML code for single movie"""
  movies = movie_storage.get_list_movies()
  seriallized_text = ""
  seriallized_text += f'<a href="{movies[single_movie]["IMDB_link"]}"><img class="movie-poster" src="{movies[single_movie]["poster"]}"></a>'
  seriallized_text += f'<div class="movie-title">{single_movie}</div>'
  seriallized_text += f'<div class="movie-year">{movies[single_movie]["year"]}</div>'
  seriallized_text += f'<div class="movie-rating">{movies[single_movie]["rating"]}</div>'
  return seriallized_text

def generate_website():
  """reads movie data and HTML template files and generates the HTML code for the website"""
  movies = movie_storage.get_list_movies()
  output = ""
  for each_movie in movies:
    output += '<li>'
    output += get_serialized_data(each_movie)
    output += '</li>'
  with open("_static/index_template.html","r") as fileobj:
    data = fileobj.read()
  with open("_static/website.html","w") as fileobj:
    updated_text = data.replace(PLACEHOLDER_TITLE,WEBSITE_TITLE).replace(PLACEHOLDER_MOVIES,output)
    fileobj.write(updated_text)
  print("Website Generated sucssefully")


def main():
  """This function shows the main functions and asks for the user input for different tasks"""
  while True:
    try:
      user_input = main_menu_and_input()
    except:
      print("\nInvalid Input\n")
      continue
    if user_input == 1 : #For listout movies
      list_of_movies()
      input("\nPress enter to continue:")
    elif user_input == 2 : #For New Movie
      new_movie = str(input("\nEnter new movie name : "))
      add_movie(new_movie)
      input("\nPress enter to continue:")
    elif user_input == 3 : #For Deleting movie
      movie_to_delet = input("\nEnter movie name to delet: ")
      delet_movie(movie_to_delet)
      input("\nPress enter to continue:")
    elif user_input == 4 : #For Updating movie
      movie_to_update = str(input("\nEnter movie name : "))
      update_movie(movie_to_update)
      input("\nPress enter to continue:")
    elif user_input == 5 : # Displaying statistics
      sorted_list_tuple,median_rating = stats()
      print(f'\nMedian rating is : {median_rating}')
      print(f'\nBest movie: {sorted_list_tuple[0][0]} , Rating : {sorted_list_tuple[0][1]}\n')
      print(f'Worst movie: {sorted_list_tuple[-1][0]} , Rating : {sorted_list_tuple[-1][1]}')
      input("\nPress enter to continue:")
    elif user_input == 6 : #If user want Random Movie
      random_choice = random_movie()
      print(f'\nYour movie for tonight: {random_choice[0]}, its rated : {random_choice[1]}')
      input("\nPress enter to continue:")
    elif user_input == 7 : #Search Movie
      search_str = str(input("\nEnter part of movie name: "))
      search_result = search_movie(search_str)
      input("\nPress enter to continue:")
    elif user_input == 8 : #For sorted movie list
      print("\n See soretd movie list by rating below:\n")
      sorted = sort_movie()
      for name,rating in sorted:
        print(f"{name} : {rating}")
      input("\nPress enter to continue:")
    elif user_input == 9:
      generate_website()
      input("\nPress enter to continue:")
    elif user_input == 0 :
      sys.exit("Bye!")

if __name__ == "__main__":
  main()
