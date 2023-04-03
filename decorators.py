import cv2 as cv

'''
Decorador para mostrar saída das funções
'''
def showImageOutput(function, title='Test'):

    def wrapper(*args, **kwargs):
        image = function(*args, **kwargs)

        if(image.shape[0] > 500 or image.shape[1] > 500):
            aspect_ratio = image.shape[0]/image.shape[1]
            resized = cv.resize(image, (500, int(500*aspect_ratio)))
            cv.imshow(title, resized)
        else:
            cv.imshow(title, image)

        cv.waitKey(0)
        
        return image
    
    return wrapper