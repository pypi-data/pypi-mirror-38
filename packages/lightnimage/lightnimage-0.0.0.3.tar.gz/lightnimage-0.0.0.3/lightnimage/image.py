import numpy as np


class Lightnimage:

    def __init__(self, img):
        """

        @param np.ndarray img: The array should be two dimensions, which means only grayscale images
        """
        self.original = img
        self.array = img

    def __sub__(self, other):
        """

        @param Lightnimage other:
        @return Lightnimage:
        """
        return Lightnimage(self.array - other.array)
