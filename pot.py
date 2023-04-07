from dataclasses import dataclass, field
from math import sqrt
import cv2 as cv
import numpy as np

'''
Contém dados sobre o bule. Assume-se que a base é achatada e que ele é simétrico em torno
do eixo perpendicular à base
'''
@dataclass
class Pot:
    height_cm : float
    basis_radius_cm : float

    def getRadiusAtHeight(self, y: int):
        raise NotImplemented

    def drawPoints(
        self, image : np.array, center : np.array, pixel_cm_ratio : float, 
        interval_cm : int = 1, point_radius=5
        ):
        im_height =  image.shape[0]
        step_im = int(interval_cm * pixel_cm_ratio)
        step_height = interval_cm

        pot_y = 0
        pixel_height = int(im_height * pixel_cm_ratio)
        pixel_center_x = center[0]
        pixel_center_y = center[1]
        cv.circle(image, (pixel_center_x, pixel_center_y), point_radius+5, (255, 255, 0), -1)
        try:
            for p in range(0, pixel_height - pixel_center_y, step_im):
                radius = self.getRadiusAtHeight(pot_y)
                pixel_radius = int(radius * pixel_cm_ratio)
                pixel_x1 = pixel_center_x - pixel_radius
                pixel_x2 = pixel_center_x + pixel_radius

                pixel_y = pixel_center_y - p
                cv.line(image, (pixel_x1, pixel_y), (pixel_x2, pixel_y), (0, 0, 255))
                cv.circle(image, (pixel_x1, pixel_y), point_radius, (0, 255, 0), -1)
                cv.circle(image, (pixel_x2, pixel_y), point_radius, (0, 255, 0), -1)

                pot_y += step_height

        except ValueError: # Y fora da elipse
            pass



'''
Assume que a elipse tem centro na origem (ponto inferior, central do bule)
e que o eixo maior é paralelo ao eixo x
https://pt.wikipedia.org/wiki/Elipse
'''

@dataclass
class PotElliptical(Pot):
    height_offset_cm : float
    coef1 : float = field(init=False)
    coef2 : float = field(init=False)

    def __post_init__(self):
        self.coef1 = self.basis_radius_cm
        self.coef2 = -(1 / (self.height_cm**2))         

    #https://math.stackexchange.com/questions/2195472/calculating-a-points-x-position-on-an-ellipse-given-pos-y
    def getRadiusAtHeight(self, y: int):
        if y <= self.height_offset_cm:
            return self.basis_radius_cm
        else:
            return self.coef1 * sqrt(1 + self.coef2 * ((y - self.height_offset_cm)**2))


if __name__ == '__main__':
    image = np.zeros((400, 400, 3), dtype=np.uint8)
    pot = PotElliptical(30, 30, 10)
    pot.drawPoints(image, (200, 300), 4 / 1, 1, 1)
    cv.imshow('Elliptical Pot', image)
    cv.waitKey(0)
