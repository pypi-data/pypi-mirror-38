# 16.11.2018
# Python 2 compatibility for the print function syntax
from __future__ import print_function

from lightnimage.image import LightningImage

from lightnimage.calculate import *

import numpy as np

from pprint import pprint

# ABSTRACT BASE CLASSES #


class AbstractVectorisationEngine:
    """

    CHANGELOG

    Added 05.11.2018

    """

    def __init__(self, lightning_image):
        """

        CHANGELOG

        Added 05.11.2018

        @param LightningImage lightning_image:
        """
        self.lightning_image = lightning_image
        self.array = self.lightning_image.array

    def __call__(self, *args, **kwargs):
        """

        CHANGELOG

        Added 05.11.2018

        @param args:
        @param kwargs:
        @return:
        """
        raise NotImplementedError()


class AbstractAreaSegmentationEngine:

    def __init__(self, config):
        pass

    def __call__(self, lightning_image):
        """
        The engine gets called on a single lightning image object and returns a list of dicts, each containing a value
        for a x, y, length and width keys, defining a rectangle, where the procedure guesses a lightning can be found

        CHANGELOG

        Added 13.11.2018

        @param lightning_image:
        @return:
        """
        raise NotImplementedError()


# IMPLEMENTATIONS #

class SimpleAreaSegmentationEngine(AbstractAreaSegmentationEngine):
    """
    This procedure assumes the image is already processed.

    Given an Image object, this algorithm will calculate the pixel sums along the rows and the columns of the picture.
    The resulting intensity function is then segmented into sub sequences along the axis's by watching, when the
    function first exceeds a certain threshold and when it drops below it again.
    From these sequences along the axis all possible combinations(=areas on the picture) are computed. These areas are
    suspected to contain intensity maximums. In the last step the average of each area is checked against another
    threshold to remove false positives from the final result.

    CHANGELOG

    Added 16.11.2018
    """
    DEFAULT_CONFIG = {
        'threshold':        1.0,
        'checking':         True,
        'check_threshold':  0.03,
    }

    def __init__(self, config):
        """
        The constructor.

        The config dict can have the following parameters:
        - threshold:        A float, which defines the factor between a value of the axis sum function and the global
                            average of the latter that qualifies a value as surpassing the threshold.
                            A threshold RELATIVE to the average of the function. DEFAULT is 1.0
        - checking:         boolean flag of whether or not to perform the last checking operation
        - check_threshold:  A float threshold value relative to 255 the average of an area has to have to qualify as a
                            valid solution to the problem. DEFAULT is 0.03, equates to roughly a grayscale value of 7,
                            which has to be the average of an area.

        CHANGELOG

        Added 16.11.2018

        @param dict config:
        """
        AbstractAreaSegmentationEngine.__init__(self, config)
        self.config = self.DEFAULT_CONFIG.copy()
        self.config.update(config)

        self.current = None

    def __call__(self, lightning_image):
        """
        The main function executed, when the engine is called.

        CHANGELOG

        Added 16.11.2018

        @param LightningImage lightning_image:
        @return: List(Tuple())
        """
        # A copy of the image object is being made, so transformations can be used without disturbing the original
        # image
        self.current = LightningImage(lightning_image)

        # Calculating the row and column sums of the grayscale values
        self.x_sums = self.current.row_sum()
        self.y_sums = self.current.column_sum()

        # Calculating the mean value of both these functions
        x_average = np.average(self.x_sums)
        y_average = np.average(self.y_sums)

        # Calculating the thresholds based on the factor given by the config
        self.x_threshold = x_average * self.config['threshold']
        self.y_threshold = y_average * self.config['threshold']

        # Getting all the possible areas
        x_sequences = threshold_sequencing(self.x_sums, self.config['threshold'])
        y_sequences = threshold_sequencing(self.y_sums, self.config['threshold'])

        areas = combinations_2d(x_sequences, y_sequences)

        if self.config['checking']:
            # Creating areas only from all the possible combinations of two axis's sub sequences also creates a lot
            # of false areas.
            # Here we go through all the areas and essentially compute the average amount of signal within them. Areas
            # are only part of the final solution, if the average within them surpasses a certain threshold
            result = []
            for area in areas:
                # Calculating the average within these areas and only using these that contain a high enough value
                av = average_2d(self.current.array, area)
                # print("Checking {} with average {}".format(str(area), av))
                if (av / 255) >= self.config['check_threshold']:
                    result.append(area)

        return result

