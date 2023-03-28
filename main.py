import cv2 as cv
import numpy as np
import os
import argparse

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
    allowed_extensions = ['.jpg', '.png']
    
    # Obtém imagem via linha de comando
    parser = argparse.ArgumentParser(
        prog = 'CoffeeVision',
        description= 'Detecta quantidade de café contido em cafeteira capturada em imagem'
    )

    parser.add_argument('filename')
    args = parser.parse_args()
    
    image_filename = args.filename
    _, ext = os.path.splitext(image_filename)
    if(ext not in allowed_extensions):
        raise ValueError('Tipos de extensão de arquivo suportadas: ' + ', '.join(allowed_extensions))

    image = np.fromfile(image_filename, dtype=np.uint8)