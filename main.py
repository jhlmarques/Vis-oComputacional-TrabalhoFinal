
from coffee_contour import *
from input_handlers import getInputImageCommandLine


if __name__ == '__main__':

    image = getInputImageCommandLine()

    # Abordagem por detecção do contorno do café e, após, do bule
    detector = CCDHSVThresholding(image)
    detector.getPercentage()

