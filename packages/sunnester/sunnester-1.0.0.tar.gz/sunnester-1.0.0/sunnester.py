def print_lol(movies_list):
    for movie in movies_list:
        if(isinstance(movie, list)):
           print_lol(movie)
        else:
           print(movie)
        
