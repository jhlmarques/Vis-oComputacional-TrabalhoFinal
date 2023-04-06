import cv2

img = cv2.imread("centroid.jpg")
currentWidth = img.shape[0]
currentHeigth = img.shape[1]

aspect_ratio = currentWidth/currentHeigth

img = cv2.resize(img, (500, int(500*aspect_ratio)))

newWidth = img.shape[0]
newHeigth = img.shape[1]

mouseX = mouseY = -1

def draw_circle(event,x,y,flags,param):
    global mouseX, mouseY
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img,(x,y), radius=3, color=(0, 0, 255), thickness=-1)
        mouseX, mouseY = mouseY,y


centroid = (int(1432/currentWidth*newWidth), int(1824/currentHeigth*newHeigth))
leftmost_centroid = (int(674/currentWidth*newWidth), int(1824/currentHeigth*newHeigth))
bottommost_centroid = (int(1432/currentWidth*newWidth), int(1981/currentHeigth*newHeigth))

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_circle)

while True:
    cv2.imshow('image', img)
    k = cv2.waitKey(1)
    if k == 27:
        cv2.destroyWindow("image")
        break

vertical_axis = (bottommost_centroid[1] - mouseY)
horizontal_axis = (centroid[0] - leftmost_centroid[0])

print(horizontal_axis, vertical_axis)

excentricity = vertical_axis/horizontal_axis

print(excentricity)

img = cv2.ellipse(img, bottommost_centroid, (horizontal_axis, vertical_axis), 180, 0, 360, (255, 0, 0), 3)

cv2.imshow('ellipse', img)
cv2.waitKey(0)
cv2.destroyWindow("ellipse")

