# Created by Q-ays.
# whosqays@gmail.com

from functools import wraps


def wrapper(f):
    @wraps(f)
    def inner():
        pass
