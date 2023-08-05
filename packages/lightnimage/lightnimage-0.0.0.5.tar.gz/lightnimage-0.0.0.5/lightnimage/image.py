import numpy as np


class Lightnimage:
    """
    A numpy array wrapper object for manipulating grayscale images

    CHANGELOG

    Added 04.11.2018

    @author Jonas Teufel
    """

    def __init__(self, img):
        """

        CHANGELOG

        Added 04.11.2018

        @param np.ndarray img: The array should be two dimensions, which means only grayscale images
        """
        self.original = img
        self.array = img

    def darken(self, threshold, replace=0):
        """

        CHANGELOG

        Added 04.11.2018

        @param int threshold:
        @param int replace:
        @return:
        """
        it = np.nditer(self.array, flags=['multi_index'], op_flags=['writeonly'])
        while not it.finished:
            if it[0] <= threshold:
                it[0] = replace
            it.iternext()

    def lighten(self, threshold, replace=255):
        """

        CHANGELOG

        Added 04.11.2018

        @param int threshold:
        @param int replace:
        @return:
        """
        it = np.nditer(self.array, flags=['multi_index'], op_flags=['writeonly'])
        while not it.finished:
            if it[0] >= threshold:
                it[0] = replace
            it.iternext()

    def subtract(self, other, threshold=10, replace=255, invert=False,):
        """

        CHANGELOG

        Added 04.11.2018

        @param Lightnimage other:   The other image, which is supposed to be subtracted from this one
        @param int threshold:
        @param int replace:
        @param bool invert:
        @return:
        """
        new = np.zeros(self.array.shape)
        it = np.nditer(new, flags=['multi_index'], op_flags=['writeonly'])
        while not it.finished:
            value_self = self.array[it.multi_index]
            value_other = other.array[it.multi_index]
            diff = abs(int(value_self) - int(value_other))

            if diff <= threshold:
                it[0] = replace
            else:
                it[0] = abs(int(value_self) - int(value_other))
                if invert:
                    it[0] = 255 - it[0]

            it.iternext()

        return Lightnimage(new)

