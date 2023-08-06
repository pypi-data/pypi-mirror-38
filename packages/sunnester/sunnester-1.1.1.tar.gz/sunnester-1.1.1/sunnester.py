def print_lol(movies_list, level):
    for movie in movies_list:
        if(isinstance(movie, list)):
           print_lol(movie, level + 1)
        else:
            for tabstop in range(level):
                print("\t", end='')
            print(movie)
        
