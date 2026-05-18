
from .models import *


# NOTE: see this function
# This function is executed automatically when the application is set up
def setup(*args, **kwargs):
    for i in range(12):
        example = Example(
            text1 = f"Random Example 1 - {i}",
            text2 = f"Random Example 2 - {i}",
            text3 = f"Random Example 3 - {i}",
            text4 = f"Random Example 4 - {i}",
            text5 = f"Random Example 5 - {i}",
            text6 = f"Random Example 6 - {i}"
        )
        example.save()
    # #endfor
# #enddef
