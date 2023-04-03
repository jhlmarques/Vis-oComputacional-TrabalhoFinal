import cv2 as cv
import numpy as np
from decorators import showImageOutput

'''
Detecta o contorno do café na imagem
'''
class CoffeeContourDetector:
    def __init__(self, image) -> None:
        self.original_image = image
    
    '''
    Realiza pré-processamento da imagem para segmentação do café via thresholding
    '''
    @showImageOutput
    def _preprocessCoffeeHSVThreshold(self, image):
        r_image = cv.GaussianBlur(image, (31,31), 1.5)
        return r_image

    '''
    Obtém o segmento contendo o café usando thresholding de cores
    '''
    @showImageOutput
    def _segmentCoffeeHSVThreshold(self, image):
        image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        hsv_brown_max = (255, 255, 90)
        hsv_brown_min = (5, 20, 5)
        return cv.inRange(image, hsv_brown_min, hsv_brown_max)

    '''
    Realiza pós-processamento da imagem contendo o segmento do café
    '''
    @showImageOutput
    def _postprocessCoffeeSegment(self, image):
        # Mais denoising
        denoised_segmented = cv.medianBlur(image, 19)#cv.GaussianBlur(segmented, (9, 9), 1)

        # Operações morfológicas
        morphed_segmented = cv.erode(denoised_segmented, (5,5), iterations=3)
        morphed_segmented = cv.dilate(morphed_segmented, (5,5))

        return morphed_segmented

    '''
    Obtém contornos do café
    '''
    def _findCoffeeContour(self, image):
        contours, _ = cv.findContours(image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        # Momentos dos contornos podem ser utilizados para obter centróides, áreas...
        # Basicamente, são os descritores da forma.
        # https://en.wikipedia.org/wiki/Image_moment
        # https://docs.opencv.org/3.4/dd/d49/tutorial_py_contour_features.html
        # https://docs.opencv.org/3.4/d1/d32/tutorial_py_contour_properties.html

        contours = self._filterContoursExtension(contours, 0.6)
        self._drawCandidateContours(contours)
        contours = self._filterContoursSolidity(contours, 0.8)
        self._drawCandidateContours(contours)
        return self._chooseBestContourByWidth(contours)

    '''
    Filtra contornos por extensão
    '''
    def _filterContoursExtension(self, contours, threshold):
        r_contours = []
        for cnt in contours:
            area = cv.contourArea(cnt)
            
            # Extent
            x,y,w,h = cv.boundingRect(cnt)
            rect_area = w*h
            extent = float(area)/rect_area

            if extent >= threshold:
                r_contours.append(cnt)
        return r_contours

    '''
    Filtra contornos por solidez
    '''
    def _filterContoursSolidity(self, contours, threshold):
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
    Decide entre contornos remanescentes com base na distância entre as extremidades horizontais
    '''
    def _chooseBestContourByWidth(self, contours):
        return max(contours, key=
        lambda cnt:
        # Direito menos esquerdo (diferença das coordenadas x)
        tuple(cnt[cnt[:,:,0].argmax()][0])[0] - tuple(cnt[cnt[:,:,0].argmin()][0])[0]
        )        

    '''
    Ajusta contorno encontrado
    '''
    def _getAdjustedBestContour(self, contour):
        return cv.convexHull(contour)

    
    '''
    Desenha contornos candidatos
    '''
    @showImageOutput
    def _drawCandidateContours(self, contours):
        image = self.original_image.copy()
        cv.drawContours(image, contours, -1, (255,0,0), thickness=3)
        return image

    '''
    Obtém contorno do café
    '''
    def getCoffeeContour(self):
        raise NotImplementedError






class CCDHSVThresholding(CoffeeContourDetector):

    def getCoffeeContour(self):
        image = self.original_image
        image = self._preprocessCoffeeHSVThreshold(image)
        image = self._segmentCoffeeHSVThreshold(image)
        image = self._postprocessCoffeeSegment(image)
        
        return self._findCoffeeContour(image)  