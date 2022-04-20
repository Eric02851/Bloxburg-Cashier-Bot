import cv2 as cv
#import numpy as np

screenshot = cv.imread('img/bloxburg4.png', cv.IMREAD_UNCHANGED)
template = cv.imread('templates/drinkTest.png', cv.IMREAD_UNCHANGED)

result = cv.matchTemplate(screenshot, template, cv.TM_CCORR_NORMED)

minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(result)

templateWidth = template.shape[1]
templateHeight = template.shape[0]

topLeft = maxLoc
bottomRight = (topLeft[0] + templateWidth, topLeft[1] + templateHeight)

cv.rectangle(screenshot, topLeft, bottomRight, color = (0, 255, 0), thickness = 2, lineType=cv.LINE_4)
print(maxVal)

cv.imshow('Result', screenshot)
cv.waitKey()