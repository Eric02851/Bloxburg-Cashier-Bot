import cv2 as cv
import time
import copy

screenshot = cv.imread('img/bloxburg1.png', cv.IMREAD_UNCHANGED)
data = {
    'burger1': {
        'color': (0,0,255)
    },
    'burger2': {
        'color': (0,165,255)
    },
    'burger3': {
        'color': (0,255,255)
    },
    'fries': {
        'color': (0,255,0)
    },
    'drink': {
        'color': (255,0,0)
    }
}

def findButtons():
    output = copy.deepcopy(data)
    output['done'] = {'color': (255,0,255)}

    for i in output:
        template = cv.imread(f'templates/buttons/{i}.png', cv.IMREAD_UNCHANGED)
        result = cv.matchTemplate(screenshot, template, cv.TM_CCORR_NORMED)

        topLeft = cv.minMaxLoc(result)[3] 
        bottomRight = topLeft[0] + template.shape[1], topLeft[1] + template.shape[0]
        center = int(topLeft[0] + (template.shape[1] / 2)), int(topLeft[1] + (template.shape[0] / 2))
        
        output[i]['topLeft'] = topLeft
        output[i]['bottomRight'] = bottomRight
        output[i]['center'] = center
    
    return output

def findOrder():
    output = copy.deepcopy(data)
    for i in output:
        template = cv.imread(f'templates/orders/{i}.png', cv.IMREAD_UNCHANGED)
        result = cv.matchTemplate(screenshot, template, cv.TM_CCORR_NORMED)

        confidence = cv.minMaxLoc(result)[1]
        output[i]['confidence'] = confidence

    return output

def main():
    start_time = time.time()
    buttons = findButtons()
    print("--- %s seconds ---" % (time.time() - start_time))

    for i in buttons:
        cv.rectangle(screenshot, buttons[i]['topLeft'], buttons[i]['bottomRight'], color = buttons[i]['color'], thickness = 4, lineType=cv.LINE_4)

    cv.imshow('Result', screenshot)
    cv.waitKey()

main()