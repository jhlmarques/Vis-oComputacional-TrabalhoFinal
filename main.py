
from coffee_contour import *
from pot import PotElliptical
from coffee_rectifier import CoffeeRectifier
from input_handlers import *
import pickle



if __name__ == '__main__':
    args = getInputCommandLine()
    image, filename = cmd_args_getInputImage(args)
    chooseHSV = cmd_args_useKnownHSVThresholds(args)

    hsv_min = None
    hsv_max = None
    hsv_data = None

    hsv_data_filename = 'hsv_values.pkl'
    if not os.path.exists(hsv_data_filename):
        with open(hsv_data_filename, 'wb') as fp:
            pickle.dump(dict(), fp)

    with open(hsv_data_filename, 'rb') as fp:
        hsv_data = pickle.load(fp)

    if (filename in hsv_data) and (not chooseHSV):
        hsv_min, hsv_max = hsv_data[filename]
    else:
        hsv_min, hsv_max = chooseHSVThreshold(image)
        hsv_data[filename] = (hsv_min, hsv_max)
        with open(hsv_data_filename, 'wb') as fp:
            pickle.dump(hsv_data, fp)


        

    print(f"Selected thresholds: {hsv_min}, {hsv_max}")
    
    pot = PotElliptical(12, 8, 2.5)


    # Detecta café, retifica baseado no formato do bule calcula proporção entre áreas do bule e do café
    detector = CCDHSVThresholding(image, hsv_min, hsv_max)
    contours = detector.getCoffeeContours()
    contours = detector.filterContoursNonZeroArea(contours)
    contours = detector.filterContoursExtension(contours, 0.6, 0.9)
    contours = detector.filterContoursWidth(contours, 500, image.shape[1])
    detector.showCandidateContours(contours)
    contours = detector.getConvexHulls(contours)
    
    rectifier = CoffeeRectifier(pot)

    best_contour_r = rectifier.findBestFittingContour(image, contours)
    best_contour = rectifier.findBestFittingContour(image, contours, False)

    output_image_r = image.copy()
    output_image = image.copy()

    print('Rotated:')
    rectifier.calculateVolume(best_contour_r)
    rectifier.drawPot(output_image_r, best_contour_r)
    print('Unrotated:')
    rectifier.calculateVolume(best_contour)
    rectifier.drawPot(output_image, best_contour)