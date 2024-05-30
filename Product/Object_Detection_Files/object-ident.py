import cv2

#thres = 0.45 # Threshold to detect object

classNames = []
classFile = "/Users/yandabao/Documents/Git/year-end-project-ayush-and-yanda-year-end-project/Product/Object_Detection_Files/coco.names"
with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = "/Users/yandabao/Documents/Git/year-end-project-ayush-and-yanda-year-end-project/Product/Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "/Users/yandabao/Documents/Git/year-end-project-ayush-and-yanda-year-end-project/Product/Object_Detection_Files/frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

mouseX = 0
mouseY = 0
bounds = []

def getObjects(img, thres, nms, draw=True, objects=[]):
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
    #print(classIds,bbox)
    if len(objects) == 0: objects = classNames
    objectInfo =[]
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId - 1]
            if className in objects:
                objectInfo.append([box,className])
                if (draw):
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

    if mouseX != 0 and mouseY != 0:
         font = cv2.FONT_HERSHEY_SIMPLEX 
         print(mouseX, ' ', mouseY) 
         cv2.putText(img, str(mouseX) + ',' +
                            str(mouseY), (mouseX,mouseY), font, 
                            1, (255, 0, 0), 2) 

    return img,objectInfo

def click_event(event, x, y, flags, params): 
  
    # checking for left mouse clicks 
    if event == cv2.EVENT_LBUTTONDOWN: 

        # displaying the coordinates 
        # on the Shell 
        print(x, ' ', y) 
        global mouseX
        global mouseY
        mouseX = x
        mouseY = y
        
        # displaying the coordinates 
        # on the image window 
                # font = cv2.FONT_HERSHEY_SIMPLEX 
                # cv2.putText(img, str(x) + ',' +
                #             str(y), (x,y), font, 
                #             1, (255, 0, 0), 2) 
        
            # checking for right mouse clicks      
            # if event==cv2.EVENT_RBUTTONDOWN: 
        
            #     # displaying the coordinates 
            #     # on the Shell 
            #     print(x, ' ', y) 
        
            #     # displaying the coordinates 
            #     # on the image window 
            #     font = cv2.FONT_HERSHEY_SIMPLEX 
            #     b = img[y, x, 0] 
            #     g = img[y, x, 1] 
            #     r = img[y, x, 2] 
            #     cv2.putText(img, str(b) + ',' +
            #                 str(g) + ',' + str(r), 
            #                 (x,y), font, 1, 
            #                 (255, 255, 0), 2) 

if __name__ == "__main__":

    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    #cap.set(10,70)
    
    while True:
        success, img = cap.read()
        result, objectInfo = getObjects(img,0.6,0.4, objects=['person'])

        # result, objectInfo = getObjects(img,0.6,0.4)
        #print(objectInfo)
        cv2.imshow("Output",img)
        cv2.setMouseCallback("Output", click_event)
        cv2.waitKey(1)