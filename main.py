import cv2 as cv
import numpy as np
import os

class CoffeeDetector:
    def __init__(self) -> None:
        pass 

    '''
    Realiza pré-processamento da imagem, obtendo novas imagens
    adequadas para o funcionamento do detector
    '''
    def preprocessImage(image : np.array) -> np.array:
        pass
        
    '''
    Retorna a porcentagem de café contido na cafeteira com base na imagem
    fornecida
    '''
    def calculateCoffePercentage(capture : np.array) -> float:
        pass


if __name__ == '__main__':
    pass