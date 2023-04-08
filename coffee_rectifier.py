from pot import Pot
from visualization import showOutput, displayImage
import cv2 as cv
import numpy as np
from math import atan

'''
Retifica um contorno de café, usando como referência um bule
'''
class CoffeeRectifier:

    def __init__(self, reference_pot : Pot) -> None:
        self.reference_pot = reference_pot

    @showOutput('Pots')
    def drawPot(self, image, cnt):
        bottommost_idx = cnt[:,:,1].argmax()
        bottommost = tuple(cnt[bottommost_idx][0])

        leftmost_idx = cnt[:,:,0].argmin()
        leftmost = tuple(cnt[leftmost_idx][0])
        rightmost_idx = cnt[:,:,0].argmax()
        rightmost = tuple(cnt[rightmost_idx][0])

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
    def findBestFittingContour(self, image, contours):

        best_cnt = None
        min_MSE = float("inf")

        for cnt in contours:

            cv.drawContours(image, [cnt], 0, (0, 0, 255), 5)
            cnt = self._rotateContour(cnt)
            cv.drawContours(image, [cnt], 0, (255, 0, 0), 5)
            
            # Ideia: pegar pontos entre a extremidade esquerda e a direita
            bottommost_idx = cnt[:,:,1].argmax()
            bottommost = tuple(cnt[bottommost_idx][0])
            leftmost_idx = cnt[:,:,0].argmin()
            leftmost = tuple(cnt[leftmost_idx][0])
            rightmost_idx = cnt[:,:,0].argmax()
            rightmost = tuple(cnt[rightmost_idx][0])
            
            candidates = cnt[rightmost_idx:leftmost_idx+1]
            for p in candidates:
                cv.circle(image, p[0], 15, (0, 255, 255), -1)
            
            pixel_radius = (rightmost[0] - leftmost[0]) // 2
            pixel_cm_ratio = pixel_radius / self.reference_pot.basis_radius_cm

            center_x = (rightmost[0] - pixel_radius)
            center_y = bottommost[1]

            # MSE?
            sum_sq_radius_diff = 0
            for p in candidates:
                x = p[0][0]
                y = p[0][1]
                y_cm = (y - center_y) / pixel_cm_ratio
                
                r = self.reference_pot.getRadiusAtHeight(y_cm)
                r_pixel = int(r * pixel_cm_ratio)
                if x < center_x:
                    expected_x = center_x - r_pixel
                else:
                    expected_x = center_x + r_pixel
                
                diff = expected_x - x
                diff = diff / pixel_cm_ratio
                sum_sq_radius_diff += diff**2
                cv.circle(image, (expected_x, y), 15, (0, 255, 0), -1)

            MSE = sum_sq_radius_diff / len(candidates)
            print(MSE)
            if MSE < min_MSE:
                min_MSE = MSE
                best_cnt = cnt

        
        cv.drawContours(image, [cnt], 0, (255, 50, 255), 15)
        displayImage('Candidatos e Selecionado', image)

        return best_cnt

    def _getContourAngle(self, cnt):
        
        leftmost_idx = cnt[:,:,0].argmin()
        left = tuple(cnt[leftmost_idx][0])
        rightmost_idx = cnt[:,:,0].argmax()
        right = tuple(cnt[rightmost_idx][0])
        
        # bottommost_idx = cnt[:,:,1].argmax()
        # leftmost_idx = cnt[:,:,0].argmin()
        # left = tuple(cnt[bottommost_idx-1][0])
        # rightmost_idx = cnt[:,:,0].argmax()
        # right = tuple(cnt[bottommost_idx+1][0])

        # Assumindo-se um contorno suficientemente bom e até certo grau de inclinação,
        # Rotacionamos a imagem baseado na inclinação da reta que passa pelas duas
        # extremidades laterais
        #https://stackoverflow.com/questions/7953316/rotate-a-point-around-a-point-with-opencv
        angle = atan((-right[1] + left[1]) / (right[0] - left[0]))

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



    @showOutput('Rotated')
    def _drawImageRotatedToContour(self, cnt, image):

        cv.drawContours(image, [cnt], 0, (0, 255, 50), 9)

        angle = self._getContourAngle(cnt)
        center = (image.shape[0]//2, image.shape[1]//2)
        center_f = (float(center[0]), float(center[1]))
        
        M = cv.getRotationMatrix2D(center_f, angle, 1)
        
        image = cv.warpAffine(image, M, image.shape[:2])

        return image




