import cv2 as cv
import time
import numpy as np
import copy
import pyautogui

data = {
    'burger1': {
        'color': (0,0,255),
        'threshold': 0.89
    },
    'burger2': {
        'color': (0,165,255),
        'threshold': 0.89
    },
    'burger3': {
        'color': (0,255,255),
        'threshold': 0.86
    },
    'fries': {
        'color': (0,255,0),
        'threshold': 0.90
    },
    'drink': {
        'color': (255,0,0),
        'threshold': 0.90
    }
}

def findButtons(screenshot):
    buttonData = copy.deepcopy(data)
    buttonData['done'] = {'color': (255,0,255)}

    for i in buttonData:
        template = cv.imread(f'templates/buttons/{i}.png')
        result = cv.matchTemplate(screenshot, template, cv.TM_CCORR_NORMED)

        topLeft = cv.minMaxLoc(result)[3] 
        bottomRight = topLeft[0] + template.shape[1], topLeft[1] + template.shape[0]
        center = int(topLeft[0] + (template.shape[1] / 2)), int(topLeft[1] + (template.shape[0] / 2))
        
        buttonData[i]['topLeft'] = topLeft
        buttonData[i]['bottomRight'] = bottomRight
        buttonData[i]['center'] = center
    
    return buttonData

def findOrder(screenshot):
    orderData = copy.deepcopy(data)
    for i in orderData:
        template = cv.imread(f'templates/orders/{i}.png')
        result = cv.matchTemplate(screenshot, template, cv.TM_CCORR_NORMED)
        imageInfo = cv.minMaxLoc(result)

        confidence = imageInfo[1]
        topLeft = imageInfo[3]
        bottomRight = topLeft[0] + template.shape[1], topLeft[1] + template.shape[0]

        orderData[i]['confidence'] = confidence
        orderData[i]['topLeft'] = topLeft
        orderData[i]['bottomRight'] = bottomRight

    order = []
    for i in orderData:
        if (orderData[i]['confidence'] >= orderData[i]['threshold']):
            order.append(i)

    return orderData, order

def main():
    #croppedImage = formattedImage[360:660, 1000:1570]
    screenshot = pyautogui.screenshot()
    screenshot = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)   

    start_time = time.time()
    buttons = findButtons(screenshot)
    print("--- %s seconds ---" % (time.time() - start_time)) 

    for i in buttons:
        cv.rectangle(screenshot, buttons[i]['topLeft'], buttons[i]['bottomRight'], buttons[i]['color'], 4, cv.LINE_4)

    cv.imshow('Result', screenshot)
    cv.waitKey()

    """
    orderData, order = findOrder()

    for i in order:
        cv.rectangle(screenshot, orderData[i]['topLeft'], orderData[i]['bottomRight'], orderData[i]['color'], 4, cv.LINE_4)
    
    print(order)
    """
    #cv.imshow('Result', screenshot)
    #cv.waitKey()
    """
    while True:
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break
    """

main()
