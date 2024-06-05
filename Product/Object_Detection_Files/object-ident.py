import cv2
import time
import threading
import tkinter as tk
from tkinter import messagebox

#thres = 0.45 # Threshold to detect object

classNames = []
classFile = "/Users/yandabao/Documents/Git/year-end-project-ayush-and-yanda-year-end-project/Product/Object_Detection_Files/coco.names"
with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = "/Users/yandabao/Documents/Git/year-end-project-ayush-and-yanda-year-end-project/Product/Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "/Users/yandabao/Documents/Git/year-end-project-ayush-and-yanda-year-end-project/Product/Object_Detection_Files/frozen_inference_graph.pb"

#define our computer vision model
net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

# mouseX = 0
# mouseY = 0

#define the variables that we'll use later on while the model is running
vision_target = None 
user_email = None
timeout_length = 10 #how long this program waits between sending emails
ready_for_email = True

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
                    desiredColor = (0, 255, 0)
                    if(vision_target == className.lower() or vision_target == className.upper()):
                        desiredColor = (0, 0, 255)
                        
                    cv2.rectangle(img,box,color=desiredColor,thickness=2)
                    cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

    # if mouseX != 0 and mouseY != 0:
    #      font = cv2.FONT_HERSHEY_SIMPLEX 
    #      print(mouseX, ' ', mouseY)
    #      cv2.putText(img, str(mouseX) + ',' +
    #                         str(mouseY), (mouseX,mouseY), font, 
    #                         1, (255, 0, 0), 2) 

    return img,objectInfo

def click_event(event, x, y, flags, params): 
  
    # checking for left mouse clicks 
    if event == cv2.EVENT_LBUTTONDOWN: 

        # displaying the coordinates 
        # on the Shell 
        print(x, ' ', y) 
        # global mouseX
        # global mouseY
        # mouseX = x
        # mouseY = y
        
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

# if __name__ == "__main__":


# Initialize variables to store the inputs

def save_input():
    global vision_target, user_email, timeout_length, ready_for_email
    vision_target = word_entry.get()
    user_email = email_entry.get()

    if vision_target and user_email:
        messagebox.showinfo("Success", "Inputs saved successfully!")
        root.destroy()
        
        start_camera_feed()

    else:
        messagebox.showwarning("Input Error", "Please fill in both fields.")


def start_camera_feed():
    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    #cap.set(10,70)
    
    while True:
        success, img = cap.read()
        # result, objectInfo = getObjects(img,0.6,0.4, objects=['person'])
        result, objectInfo = getObjects(img,0.6,0.4)

        for pair in objectInfo:
            if pair[1] == vision_target.lower() or pair[1] == vision_target.upper():
                if ready_for_email:
                    email_thread = threading.Thread(target=send_email, args=(10,))
                    # Start the timer thread
                    email_thread.start()
                            
        cv2.imshow("Output",img)
        # cv2.setMouseCallback("Output", click_event)
        cv2.waitKey(1)
            
def send_email(seconds):
    global ready_for_email
    ready_for_email = False
    print("email sent")
    time.sleep(seconds)
    ready_for_email = True

# Create the main window
root = tk.Tk()
root.title("Input Saver")

# Create and place the word label and entry
word_label = tk.Label(root, text="Enter a vision target:")
word_label.pack(pady=5)
word_entry = tk.Entry(root)
word_entry.pack(pady=5)

# Create and place the email label and entry
email_label = tk.Label(root, text="Enter an email:")
email_label.pack(pady=5)
email_entry = tk.Entry(root)
email_entry.pack(pady=5)

# Create and place the submit button
submit_button = tk.Button(root, text="Submit", command=save_input)
submit_button.pack(pady=20)

# Run the application
root.mainloop()

# Print the stored variables after the window is closed