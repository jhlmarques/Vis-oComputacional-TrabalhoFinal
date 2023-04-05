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
    @showImageOutput('Pre-process')
    def _preprocessCoffeeHSVThreshold(self, image):
        r_image = cv.GaussianBlur(image, (31,31), 15)
        return r_image

    '''
    Obtém o segmento contendo o café usando thresholding de cores
    '''
    @showImageOutput('HSV Thresholding')
    def _segmentCoffeeHSVThreshold(self, image):
        image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        # Regiões marrons
        hsv_brown_max = (41, 189, 91)
        hsv_brown_min = (0, 31, 0)

        r_image = cv.inRange(image, hsv_brown_min, hsv_brown_max)


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

    '''
    Obtém contornos do café
    '''
    def _findCoffeeContour(self, image):
        contours, _ = cv.findContours(image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        self._drawCandidateContours(contours)
        # Momentos dos contornos podem ser utilizados para obter centróides, áreas...
        # Basicamente, são os descritores da forma.
        # https://en.wikipedia.org/wiki/Image_moment
        # https://docs.opencv.org/3.4/dd/d49/tutorial_py_contour_features.html
        # https://docs.opencv.org/3.4/d1/d32/tutorial_py_contour_properties.html

        contours = self._filterContoursNonZeroArea(contours)
        #self._drawCandidateContours(contours)

        # contours = self._filterContoursSolidity(contours, 0.8) # Must come before getting the convex hulls
        # self._drawCandidateContours(contours) 
        contours = self._getConvexHulls(contours)
        self._drawCandidateContours(contours)

        contours = self._filterContoursExtension(contours, 0.5, 0.9)
        self._drawCandidateContours(contours)
        
        contours = self._filterContoursExtremitiesTangent(contours, 0.1)
        self._drawCandidateContours(contours)

        r_cnt = self._chooseBestContourByWidth(contours)
        self._drawCandidateContours([r_cnt])
        return r_cnt

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
    def _filterContoursNonZeroArea(self, contours):
        r_contours = []
        for cnt in contours:
            if cv.contourArea(cnt) != 0:
                r_contours.append(cnt)
        return r_contours

    '''
    Filtra contornos por extensão
    '''
    def _filterContoursExtension(self, contours, threshold1, threshold2):
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
    Filtra contornos pela inclinação da reta que passa pelas extremidades horizontais
    '''
    def _filterContoursExtremitiesTangent(self, contours, threshold):
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
    def _chooseBestContourByWidth(self, contours):
        return max(contours, key=
        lambda cnt:
        # Direito menos esquerdo (diferença das coordenadas x)
        tuple(cnt[cnt[:,:,0].argmax()][0])[0] - tuple(cnt[cnt[:,:,0].argmin()][0])[0]
        )        

    
    '''
    Desenha contornos candidatos
    '''
    @showImageOutput('Contornos')
    def _drawCandidateContours(self, contours):
        image = self.original_image.copy()
        cv.drawContours(image, contours, -1, (255,0,0), thickness=7)
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