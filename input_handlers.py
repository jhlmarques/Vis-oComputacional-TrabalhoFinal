import os, argparse
import numpy as np
import cv2 as cv

'''
Obtém dados de input do programa
'''
def getInputCommandLine():

    # Obtém imagem via linha de comando
    parser = argparse.ArgumentParser(
        prog = 'CoffeeVision',
        description= 'Detecta quantidade de café contido em cafeteira capturada em imagem'
    )

    parser.add_argument('filename')
    parser.add_argument('-c','--chooseHSV', action='store_true')
    args = parser.parse_args()
    
    return args

def cmd_args_getInputImage(args):
    allowed_extensions = ['.jpg', '.png']
    image_filename = args.filename
    _, ext = os.path.splitext(image_filename)
    if(ext not in allowed_extensions):
        raise ValueError('Tipos de extensão de arquivo suportadas: ' + ', '.join(allowed_extensions))

    return cv.imdecode(np.fromfile(image_filename, dtype=np.uint8), cv.IMREAD_COLOR), image_filename

def cmd_args_useKnownHSVThresholds(args):
    return args.chooseHSV


def chooseHSVThreshold(img):
    SAT_VAL_MAX_VALUE = 255
    HUE_MAX_VALUE = 179

    hsv_max = [0, 0, 0]
    hsv_min = [0, 0, 0]

    if(img.shape[0] > 500 or img.shape[1] > 500):
        aspect_ratio = img.shape[0]/img.shape[1]
        img = cv.resize(img, (500, int(500*aspect_ratio)))

    # Create a window
    cv.namedWindow('trackbars', cv.WINDOW_NORMAL)


    # create trackbars for color change
    # Hue is from 0-179 for Opencv
    cv.createTrackbar('Min Hue', 'trackbars', 0, HUE_MAX_VALUE,
                      lambda val: change_min(val, 0, hsv_min))
    cv.createTrackbar('Min Sat', 'trackbars', 0, SAT_VAL_MAX_VALUE,
                      lambda val: change_min(val, 1, hsv_min))
    cv.createTrackbar('Min Val', 'trackbars', 0, SAT_VAL_MAX_VALUE,
                      lambda val: change_min(val, 2, hsv_min))
    cv.createTrackbar('Max Hue', 'trackbars', 0, HUE_MAX_VALUE,
                      lambda val: change_max(val, 0, hsv_max))
    cv.createTrackbar('Max Sat', 'trackbars', 0, SAT_VAL_MAX_VALUE,
                      lambda val: change_max(val, 1, hsv_max))
    cv.createTrackbar('Max Val', 'trackbars', 0, SAT_VAL_MAX_VALUE,
                      lambda val: change_max(val, 2, hsv_max))

    cv.setTrackbarPos('Max Hue', 'trackbars', 179)
    cv.setTrackbarPos('Max Sat', 'trackbars', 255)
    cv.setTrackbarPos('Max Val', 'trackbars', 255)

    while (True):
        # Set minimum and max HSV values to display
        lower = np.array(hsv_min)
        upper = np.array(hsv_max)

        # Create HSV Image and threshold into a range.
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv, lower, upper)
        output = cv.bitwise_and(img, img, mask=mask)
            
        # Display output output
        cv.imshow('output', output)

        # Exit condition ----------------------
        if cv.waitKey(20) & 0xFF == 27:
            break

    cv.destroyAllWindows()
    
    return np.array(hsv_min), np.array(hsv_max)

def change_min(val, index, hsv_min):
    hsv_min[index] = val


def change_max(val, index, hsv_max):
    hsv_max[index] = val
