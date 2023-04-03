import os, argparse
import numpy as np
import cv2 as cv

'''
Obtém a imagem a ser usada como input para o programa
'''
def getInputImageCommandLine():
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

    return cv.imdecode(np.fromfile(image_filename, dtype=np.uint8), cv.IMREAD_COLOR)