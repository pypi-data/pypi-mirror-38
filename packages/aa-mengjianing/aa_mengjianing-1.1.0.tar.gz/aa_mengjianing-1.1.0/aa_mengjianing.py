"" "递归调用" ""
def eachMovies(movies, levels=0):
        for each_item in movies:
                if isinstance(each_item, list):
                        eachMovies(each_item,levels+1)
                else :
                        for tab_stop in range(levels):
                                print("\t",end='')
                        print(each_item)
