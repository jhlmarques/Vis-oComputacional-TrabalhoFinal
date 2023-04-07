
from coffee_contour import *
from pot import PotElliptical
from coffee_rectifier import CoffeeRectifier
from input_handlers import getInputImageCommandLine


if __name__ == '__main__':

    image = getInputImageCommandLine()

    # Detecta café, retifica baseado no formato do bule e retifica
    detector = CCDHSVThresholding(image)
    cnt = detector.getCoffeeContour()
    pot = PotElliptical(12, 8, 2.5)
    rectifier = CoffeeRectifier(pot)
    rectifier.drawUnrectified(image, cnt)
