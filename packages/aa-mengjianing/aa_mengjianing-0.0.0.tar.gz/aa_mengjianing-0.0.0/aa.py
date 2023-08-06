"""递归调用"""
#sdfsf
def eachMovies(movies):
	for each_item in movies:
		if isinstance(each_item,list):
			eachMovies(each_item)
		else:
			print(each_item)
