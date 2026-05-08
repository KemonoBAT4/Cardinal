
from .models import *


# NOTE: see this function
# This function is executed automatically when the application is set up
def setup(*args, **kwargs):
    for i in range(12):
        movie = Movie(
            title = f"Movie {i}",
            description = f"Description {i}",
            movie_file_name = f"movie{i}.mp4"
        )
        movie.save()
    # #endfor
# #enddef
