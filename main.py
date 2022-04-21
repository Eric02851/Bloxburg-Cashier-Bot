import cv2 as cv
import time
import copy

screenshot = cv.imread('img/order/bloxburg4.png', cv.IMREAD_UNCHANGED)
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

def findButtons():
    buttonData = copy.deepcopy(data)
    buttonData['done'] = {'color': (255,0,255)}

    for i in buttonData:
        template = cv.imread(f'templates/buttons/{i}.png', cv.IMREAD_UNCHANGED)
        result = cv.matchTemplate(screenshot, template, cv.TM_CCORR_NORMED)

        topLeft = cv.minMaxLoc(result)[3] 
        bottomRight = topLeft[0] + template.shape[1], topLeft[1] + template.shape[0]
        center = int(topLeft[0] + (template.shape[1] / 2)), int(topLeft[1] + (template.shape[0] / 2))
        
        buttonData[i]['topLeft'] = topLeft
        buttonData[i]['bottomRight'] = bottomRight
        buttonData[i]['center'] = center
    
    return buttonData

def findOrder():
    orderData = copy.deepcopy(data)
    for i in orderData:
        template = cv.imread(f'templates/orders/{i}.png', cv.IMREAD_UNCHANGED)
        result = cv.matchTemplate(screenshot, template, cv.TM_CCORR_NORMED)

        confidence = cv.minMaxLoc(result)[1]
        orderData[i]['confidence'] = confidence

    output = []
    for i in orderData:
        if (orderData[i]['confidence'] >= orderData[i]['threshold']):
            output.append(i)

    return output

def main():
    #start_time = time.time()
    #buttons = findButtons()
    #print("--- %s seconds ---" % (time.time() - start_time))

    #for i in buttons:
     #   cv.rectangle(screenshot, buttons[i]['topLeft'], buttons[i]['bottomRight'], color = buttons[i]['color'], thickness = 4, lineType=cv.LINE_4)

    order = findOrder()
    print(order)

    #cv.imshow('Result', screenshot)
    #cv.waitKey()

main()