import cv2 as cv
import numpy as np
from decorators import showImageOutput

# Momentos dos contornos podem ser utilizados para obter centróides, áreas...
# Basicamente, são os descritores da forma.
# https://en.wikipedia.org/wiki/Image_moment
# https://docs.opencv.org/3.4/dd/d49/tutorial_py_contour_features.html
# https://docs.opencv.org/3.4/d1/d32/tutorial_py_contour_properties.html


'''
Detecta o contorno do café na imagem
'''
class CoffeeContourDetector:
    def __init__(self, image) -> None:
        self.original_image = image
    
    @showImageOutput('Original Image')
    def showOriginalImage(self):
        return self.original_image

    '''
    Obtém contornos do café
    '''
    def _findCoffeeContours(self, image):
        contours, _ = cv.findContours(image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        self.showCandidateContours(contours)
        return contours

    '''
    Obtém convex hull dos contornos
    '''
    def _getConvexHulls(self, contours):
        r_contours = []
        for cnt in contours:
            r_contours.append(cv.convexHull(cnt))
        return r_contours
    
    '''
    Filtra contornos que tem área 0
    '''
    def filterContoursNonZeroArea(self, contours):
        r_contours = []
        for cnt in contours:
            if cv.contourArea(cnt) != 0:
                r_contours.append(cnt)
        return r_contours

    '''
    Filtra contornos por extensão
    '''
    def filterContoursExtension(self, contours, threshold1, threshold2):
        r_contours = []
        for cnt in contours:
            area = cv.contourArea(cnt)
            
            # Extent
            x,y,w,h = cv.boundingRect(cnt)
            rect_area = w*h
            extent = float(area)/rect_area

            if extent >= threshold1 and extent <= threshold2:
                r_contours.append(cnt)
        return r_contours

    '''
    Filtra contornos por solidez
    '''
    def filterContoursSolidity(self, contours, threshold):
        r_contours = []
        for cnt in contours:
            area = cv.contourArea(cnt)
            
            # Solidity
            hull = cv.convexHull(cnt)
            hull_area = cv.contourArea(hull)
            solidity = float(area)/hull_area

            if solidity >= threshold:
                r_contours.append(cnt)
        return r_contours
    
    '''
    Filtra contornos pela inclinação da reta que passa pelas extremidades horizontais
    '''
    def filterContoursExtremitiesTangent(self, contours, threshold):
        r_contours = []
        for cnt in contours:

            rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
            leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
            x_diff = rightmost[0] - leftmost[0]
            y_diff = rightmost[1] - leftmost[1]
            if x_diff == 0:
                continue
            
            ang_coeff = y_diff / x_diff
            
            if abs(ang_coeff) <= threshold:
                r_contours.append(cnt)
        return r_contours        

    '''
    Decide entre contornos remanescentes com base na distância entre as extremidades horizontais
    '''
    def filterContoursWidth(self, contours, min_width, max_width):
        r_contours = []
        for cnt in contours:
            x1 = tuple(cnt[cnt[:,:,0].argmin()][0])[0]
            x2 = tuple(cnt[cnt[:,:,0].argmax()][0])[0]
            width = x2 - x1
            if (width >= min_width) and (width <= max_width):
                r_contours.append(cnt)
        return r_contours

    '''
    Desenha contornos candidatos
    '''
    @showImageOutput('Contornos')
    def showCandidateContours(self, contours):
        image = self.original_image.copy()
        cv.drawContours(image, contours, -1, (255,0,0), thickness=7)
        return image

    '''
    Obtém contorno do café
    '''
    def getCoffeeContours(self):
        raise NotImplementedError

    '''
    Obtém contorno do bule
    '''
    def getPotContour(self):
        raise NotImplementedError






class CCDHSVThresholding(CoffeeContourDetector):
    
    def __init__(self, image, hsv_brown_min, hsv_brown_max) -> None:
        super().__init__(image)
        self.hsv_brown_max = hsv_brown_max
        self.hsv_brown_min = hsv_brown_min

    
    '''
    Realiza pré-processamento da imagem para segmentação do café via thresholding
    '''
    @showImageOutput('Pre-process')
    def _preprocessCoffeeHSVThreshold(self, image):
        r_image = cv.GaussianBlur(image, (31,31), 15)
        return r_image

    '''
    Obtém o segmento contendo o café usando thresholding de cores
    '''
    @showImageOutput('HSV Thresholding')
    def _segmentCoffeeHSVThreshold(self, image, thresh_min, thresh_max):
        image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        r_image = cv.inRange(image, thresh_min, thresh_max)
        return r_image

    '''
    Realiza pós-processamento da imagem contendo o segmento do café
    '''
    @showImageOutput('Post Process')
    def _postprocessCoffeeSegment(self, image):
        # Mais denoising
        #image = cv.medianBlur(image, 5)
        #image = cv.GaussianBlur(image, (25, 25), 5)

        # Operações morfológicas
        #image = cv.morphologyEx(image, cv.MORPH_CLOSE, kernel=(5,5), iterations=40)
        #image = cv.dilate(image, (9,9), iterations=9)
       # image = cv.erode(image, (3,3), iterations=3)

        return image


    def _findCoffeeContours(self, image):
        contours = super()._findCoffeeContours(image)
        return self._getConvexHulls(contours)

    def getCoffeeContours(self):
        image = self.original_image
        image = self._preprocessCoffeeHSVThreshold(image)
        image = self._segmentCoffeeHSVThreshold(image, self.hsv_brown_min, self.hsv_brown_max)
        image = self._postprocessCoffeeSegment(image)
        contours = self._findCoffeeContours(image)
        #cnt = self._chooseBestContourByWidth(contours)
        
        return contours  
