import cv2 as cv

'''
Decorador para mostrar saída das funções
'''
def showOutput(title):
    def decorator(function):
        def wrapper(*args, **kwargs):
            image = function(*args, **kwargs)     
            displayImage(title, image)
            return image
        return wrapper
    
    return decorator

def getScaledImage(image):
    if(image.shape[0] > 500 or image.shape[1] > 500):
        aspect_ratio = image.shape[0]/image.shape[1]
        image = cv.resize(image, (500, int(500*aspect_ratio)))
    
    return image

def displayImage(title, image):
    image = getScaledImage(image)
    cv.imshow(title, image)
    cv.waitKey(0)
    cv.destroyWindow(title)