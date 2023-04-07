
from coffee_contour import *
from pot import PotElliptical
from coffee_rectifier import CoffeeRectifier
from input_handlers import getInputImageCommandLine, chooseHSVThreshold




if __name__ == '__main__':

    image = getInputImageCommandLine()
    hsv_min, hsv_max = chooseHSVThreshold(image)
    print(f"Selected thresholds: {hsv_min}, {hsv_max}")
    
    pot = PotElliptical(12, 8, 2.5)


    # Detecta café, retifica baseado no formato do bule e retifica
    detector = CCDHSVThresholding(image, hsv_min, hsv_max)
    contours = detector.getCoffeeContours()
    contours = detector.filterContoursNonZeroArea(contours)
    contours = detector.filterContoursExtension(contours, 0.6, 0.9)
    contours = detector.filterContoursWidth(contours, 50, image.shape[1])
    detector.showCandidateContours(contours)
    rectifier = CoffeeRectifier(pot)
    for cnt in contours:
        rectifier.drawUnrectified(image, cnt)
