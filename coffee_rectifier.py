from pot import Pot
from decorators import showImageOutput
import cv2 as cv
import numpy as np
from math import atan

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

    '''
    Decide qual o melhor contorno baseado em quão bem ele se adequa às bordas da bule
    '''
    @showImageOutput('Rotacionados')
    def getBestFittingContour(self, image, contours):

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

        for cnt in contours:

            #self._drawImageRotatedToContour(cnt, image)
            cv.drawContours(image, [cnt], 0, (0, 0, 255), 5)
            cnt = self._rotateContour(cnt)
            cv.drawContours(image, [cnt], 0, (255, 0, 0), 5)
           


            # # Assumindo-se que o ponto mais
            # contours_bottom_left = cnt[bottommost_idx:leftmost_idx+1]
            # contours_bottom_right = cnt[rightmost_idx:bottommost_idx+1]
        return image            

    def _getContourAngle(self, cnt):
        leftmost_idx = cnt[:,:,0].argmin()
        leftmost = tuple(cnt[leftmost_idx][0])
        rightmost_idx = cnt[:,:,0].argmax()
        rightmost = tuple(cnt[rightmost_idx][0])

        # Assumindo-se um contorno suficientemente bom e até certo grau de inclinação,
        # Rotacionamos a imagem baseado na inclinação da reta que passa pelas duas
        # extremidades laterais
        #https://stackoverflow.com/questions/7953316/rotate-a-point-around-a-point-with-opencv
        angle = atan((rightmost[1] - leftmost[1]) / (rightmost[0] - leftmost[0]))
        # Convert to degrees
        angle = angle * (180 / np.pi)
        return angle

    def cart2pol(self, x, y):
        theta = np.arctan2(y, x)
        rho = np.hypot(x, y)
        return theta, rho

    def pol2cart(self, theta, rho):
        x = rho * np.cos(theta)
        y = rho * np.sin(theta)
        return x, y

    #https://medium.com/analytics-vidhya/tutorial-how-to-scale-and-rotate-contours-in-opencv-using-python-f48be59c35a2
    def _rotateContour(self, cnt):
        # Obtém ângulo
        angle = self._getContourAngle(cnt)

        M = cv.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        # Translada contorno pro centróide
        cnt_norm = cnt - [cx, cy]

        # Obtém coordenadas polares de cada ponto do contorno
        coordinates = cnt_norm[:, 0, :]
        xs, ys = coordinates[:, 0], coordinates[:, 1]
        thetas, rhos = self.cart2pol(xs, ys)

        # Soma ângulo
        thetas_deg = np.rad2deg(thetas)
        thetas_new_deg = (thetas_deg + angle) % 360
        thetas_new = np.deg2rad(thetas_new_deg)

        # Converte de volta a coordenadas cartesianas
        xs, ys = self.pol2cart(thetas_new, rhos)
        cnt_norm[:, 0, 0] = xs
        cnt_norm[:, 0, 1] = ys
        cnt_rotated = cnt_norm + [cx, cy]
        cnt_rotated = cnt_rotated.astype(np.int32)

        return cnt_rotated



    @showImageOutput('Rotated')
    def _drawImageRotatedToContour(self, cnt, image):

        cv.drawContours(image, [cnt], 0, (0, 255, 50), 9)

        angle = self._getContourAngle(cnt)
        center = (image.shape[0]//2, image.shape[1]//2)
        center_f = (float(center[0]), float(center[1]))
        
        M = cv.getRotationMatrix2D(center_f, angle, 1)
        
        image = cv.warpAffine(image, M, image.shape[:2])

        return image

    def rectify(contour):
        pass



