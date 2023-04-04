import cv2 as cv
import numpy as np

SAT_VAL_MAX_VALUE = 255
HUE_MAX_VALUE = 179

hsv_max = [0, 0, 0]
hsv_min = [0, 0, 0]


def change_min(val, index):
    hsv_min[index] = val


def change_max(val, index):
    hsv_max[index] = val


# ---------------------- MAIN CODE ---------------------- #
if __name__ == "__main__":
    # Create a window
    cv.namedWindow('trackbars', cv.WINDOW_NORMAL)
    cv.namedWindow('image', cv.WINDOW_NORMAL)

    # create trackbars for color change
    # Hue is from 0-179 for Opencv
    cv.createTrackbar('Min Hue', 'trackbars', 0, HUE_MAX_VALUE,
                      lambda val: change_min(val, 0))
    cv.createTrackbar('Min Sat', 'trackbars', 0, SAT_VAL_MAX_VALUE,
                      lambda val: change_min(val, 1))
    cv.createTrackbar('Min Val', 'trackbars', 0, SAT_VAL_MAX_VALUE,
                      lambda val: change_min(val, 2))
    cv.createTrackbar('Max Hue', 'trackbars', 0, HUE_MAX_VALUE,
                      lambda val: change_max(val, 0))
    cv.createTrackbar('Max Sat', 'trackbars', 0, SAT_VAL_MAX_VALUE,
                      lambda val: change_max(val, 1))
    cv.createTrackbar('Max Val', 'trackbars', 0, SAT_VAL_MAX_VALUE,
                      lambda val: change_max(val, 2))

    # Set default value for MAX HSV trackbars.
    cv.setTrackbarPos('Max Hue', 'trackbars', 179)
    cv.setTrackbarPos('Max Sat', 'trackbars', 255)
    cv.setTrackbarPos('Max Val', 'trackbars', 255)

    img = cv.imread('images/20230330_143258.jpg')

    while (True):
        # Set minimum and max HSV values to display
        lower = np.array(hsv_min)
        upper = np.array(hsv_max)

        # Create HSV Image and threshold into a range.
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv, lower, upper)
        output = cv.bitwise_and(img, img, mask=mask)

        # Display output image
        cv.imshow('image', output)

        # Exit condition ----------------------
        if cv.waitKey(20) & 0xFF == 27:
            break

    cv.destroyAllWindows()
