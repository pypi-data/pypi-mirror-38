import numpy as np

import copy


class LightningImage:
    """
    A numpy array wrapper object for manipulating grayscale images.

    CHANGELOG

    Added 04.11.2018

    @author Jonas Teufel
    """

    def __init__(self, img):
        """
        The constructor.

        CHANGELOG

        Added 04.11.2018

        Changed 06.11.2018
        Added separate attributes for the height and width of the image

        Changed 13.11.2018
        Now a LightningImage object can be passed to the constructor, which will result in the
        creation of a copy of that image.
        Added a original field

        @param np.ndarray img: The array should be two dimensions, which means only grayscale images
        """
        if isinstance(img, LightningImage):
            # If the input was another lightning image object it gets copied, which means
            # the original also gets copied
            self.array = copy.deepcopy(img.array)
            self.original = copy.deepcopy(img.original)
        else:
            self.array = copy.deepcopy(img)
            self.original = copy.deepcopy(img)

        # 06.11.2018
        # Saving the height and the width of the image and thus the dimensions of the array as well
        self.width = self.array.shape[1]
        self.height = self.array.shape[0]

    def darken(self, threshold, replace=0):
        """
        This method will select all the pixels with the grayscale value LOWER than the given threshold and replace them
        with the given fixed value 'replace'. The default to replace with is 0(dark), thus darkening the pixels
        CHANGELOG

        Added 04.11.2018

        @param int threshold:   All the pixels, that are smaller than this will be replaced. This has to be 8 bit int
        @param int replace:     The fixed value to replace with
        @return: void
        """
        it = np.nditer(self.array, flags=['multi_index'], op_flags=['writeonly'])
        while not it.finished:
            if it[0] <= threshold:
                it[0] = replace
            it.iternext()

    def lighten(self, threshold, replace=255):
        """
        This method will select all the pixels with a grayscale value BIGGER than the given threshold and replace them
        with the given fixed value 'replace'. The default to replace with is 255(white) thus lightening those pixels up

        CHANGELOG

        Added 04.11.2018

        @param int threshold:   All values, that are bigger than this will be replaced. This has to be in the range 0
                                to 255
        @param int replace:     The fixed value to replace all the pixels with, that are bigger than the threshold
        @return: void
        """
        it = np.nditer(self.array, flags=['multi_index'], op_flags=['writeonly'])
        while not it.finished:
            if it[0] >= threshold:
                it[0] = replace
            it.iternext()

    def invert(self):
        """
        Inverts all the grayscale values of all the pixels of the picture

        CHANGELOG

        Added 04.11.2018

        @return: void
        """
        it = np.nditer(self.array, flags=['multi_index'], op_flags=['writeonly'])
        while not it.finished:
            it[0] = 255 - it[0]
            it.iternext()

    def difference(self, other, threshold=10, replace=255, invert=False, ):
        """
        This method will essentially substract two images with one another. But it will do so in a commutative way,
        which means that for each pixel the absolute difference is being calculated, which prevents negative values,
        but also means, that the operation does not have an order.
        Additionally all resulting differences lower than a 'threshold' can be replaced by a fixed values 'replace'.
        This is to be able to remove noise from the picture, as small differences in two different pictures of the
        same thing are most likely to be random noise.


        why not just a plain & normal subtraction?
        Because the numpy arrays, which represent images use unsigned 8 bit integers and if the result of one pixel
        subtraction will be negative, this will cause the data type to start at the other end again instead.
        Example: 0 - 1 = 254

        CHANGELOG

        Added 04.11.2018

        @param LightningImage other:    The other image, which is supposed to be subtracted from this one
        @param int threshold:           Every resulting difference value below this given int will be replaced with a
                                        fixed value. If this is 0 no replacements will be made
        @param int replace:             The value to replace pixels with, that are below the threshold
        @param bool invert:
        @return LightningImage:         The new image
        """
        new = np.zeros(self.array.shape)
        it = np.nditer(new, flags=['multi_index'], op_flags=['writeonly'])
        while not it.finished:
            value_self = self.array[it.multi_index]
            value_other = other.array[it.multi_index]
            diff = abs(int(value_self) - int(value_other))

            if diff < threshold:
                it[0] = replace
            else:
                it[0] = abs(int(value_self) - int(value_other))
                if invert:
                    it[0] = 255 - it[0]

            it.iternext()

        return LightningImage(new)

    def column_sum(self, scale=None):
        """
        Calculates an array, that contains the float sum's of all the elements of each column. he resulting array can
        optionally be scaled relative to a new peak value. The resulting array has as many elements as the image's
        width

        CHANGELOG

        Added 06.11.2018

        @param scale:   The new peak value to scale to. DEFAULT is None, which means no scaling will be done
        @return:
        """
        # This is just a special case of the general case 'directional_sum', which is a implementation for both
        # directions
        return self.directional_sum(0, scale)

    def row_sum(self, scale=None):
        """
        Calculates an array, that contains the float sum's of all the elements of each row. The resulting array can
        optionally be scaled relative to a new peak value. The resulting array has as many elements as the image's
        height

        CHANGELOG

        Added 06.11.2018

        @param scale:   The new peak value to scale to. DEFAULT is None, which means no scaling will be done
        @return:
        """
        # This is just a special case of the general case 'directional_sum', which is a implementation for both
        # directions
        return self.directional_sum(1, scale)

    def directional_sum(self, axis, scale):
        """
        Calculates an array, that contains the float sum's of each element either the rows or the columns. The array
        thus has the same size as either the column or the row of the image.
        These sum values could possibly take any value from 0 to 255 * array length (for an all white picture). The
        scale parameter optionally limits the maximum value possible by scaling all elements down proportionally.

        CHANGELOG

        Added 06.11.2018

        @param int axis:    Either 0 or 1. A 1 would be the sum of all rows and 0 the sum of all columns
        @param int scale:   An integer, which sets the maximum value for the sums. All values get scaled
                            relative to this value.
        @return: An array of either the height or width of the image
        """

        # Creating a new one dimensional array with just as many elements as there are pixel rows in the image, which
        # will contain the sum values of each row.
        # For a two dimensional array (as the image is one), the second item of the shape attribute will contain the
        # length of a column and thus the amount of rows
        sum_array = np.ndarray(self.array.shape[axis], np.float64)

        # Iterating through all the rows of the array ans summing up the individual elements
        for i in range(self.array.shape[axis]):
            temp_sum = 0
            for j in range(self.array.shape[1 - axis]):
                # Numpy arrays support multi indexing in a single bracket for higher dimensions and this is also the
                # more efficient way
                if axis:
                    temp_sum += self.array[j, i] # lol
                else:
                    temp_sum += self.array[i, j] # lol

            sum_array[i] = temp_sum

        # If there is a scale value given, all the values in the array will be scaled, so that the maximum value is
        # at most the scale value
        if scale is not None:
            maximum = max(sum_array)
            # The np.vectorize function is used to convert a normal python function object into a function, that can
            # be applied on a numpy array, element-wise
            scaling = np.vectorize(lambda x: (x / maximum) * scale, otypes=[np.float64])
            sum_array = scaling(sum_array)

        return sum_array

    def __sub__(self, other):
        """
        The subtraction operation.

        This creates a new image object, where each pixel of the resulting image has the absolute difference of the
        two initial pictures as the grayscale value.

        CHANGELOG

        Added 06.11.2018

        @param LightningImage other:   The image to be subtracted
        @return: LightningImage
        """
        # The pure subtraction is just a special case of the general difference function, but without the whole noise
        # replacement function
        return self.difference(other, threshold=0)
