from pot import Pot
from decorators import showImageOutput
import cv2 as cv
import numpy as np

'''
Retifica um contorno de café, usando como referência um bule
'''
class CoffeeRectifier:

    def __init__(self, reference_pot : Pot) -> None:
        self.reference_pot = reference_pot

    @showImageOutput('Unrectified')
    def drawUnrectified(self, image, cnt):
        bottommost_idx = cnt[:,:,1].argmax()
        bottommost = tuple(cnt[bottommost_idx][0])

        leftmost_idx = cnt[:,:,0].argmin()
        leftmost = tuple(cnt[leftmost_idx][0])
        rightmost_idx = cnt[:,:,0].argmax()
        rightmost = tuple(cnt[rightmost_idx][0])

        # contours_bottom_left = cnt[bottommost_idx:leftmost_idx+1]
        # contours_bottom_right = cnt[rightmost_idx:bottommost_idx+1]
        # cv.drawContours(image, contours_bottom_left, -1, (255, 0, 0), thickness=30)
        # cv.drawContours(image, contours_bottom_right, -1, (0, 255, 0), thickness=30)

        # title = 'Bottom-left'
        # if(image.shape[0] > 500 or image.shape[1] > 500):
        #     aspect_ratio = image.shape[0]/image.shape[1]
        #     resized = cv.resize(image, (500, int(500*aspect_ratio)))
        #     cv.imshow(title, resized)
        # else:
        #     cv.imshow(title, image)
        # cv.waitKey(0)

        
        pixel_radius = (rightmost[0] - leftmost[0]) // 2
        pixel_cm_ratio = pixel_radius / self.reference_pot.basis_radius_cm
        center_x = (rightmost[0] - pixel_radius)
        center_y = bottommost[1]

        cv.drawContours(image, [cnt], 0, (255, 0, 0), thickness=15)
        self.reference_pot.drawPoints(image, (center_x, center_y), pixel_cm_ratio, 0.1, point_radius=15)

        return image


    def rectify(contour):
        pass



