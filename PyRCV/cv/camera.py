import cv2, sys, time, os

# Load the BCM V4l2 driver for /dev/video0. This driver has been installed from earlier terminal commands. 
#This is really just to ensure everything is as it should be.
os.system('sudo modprobe bcm2835-v4l2')
# Set the framerate (not sure this does anything! But you can change the number after | -p | to allegedly increase or decrease the framerate).
os.system('v4l2-ctl -p 40')

class camera():

    def __init__(self,screen):
        self.screen = screen
        self.object_x = 0
        self.object_y = 0

    def faceDetection(self):
        """
        Function for CV of faces, with OpenCV models.
        """
        
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH,  self.screen[0]);
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.screen[1]);
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            # This line lets you mount the camera the "right" way up, with neopixels above
            #frame = cv2.flip(frame, -1)
            
            if ret == False:
                print("Error getting image")
                continue

            # Convert to greyscale for easier faster accurate face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist( gray )

            # Do face detection to search for faces from these captures frames
            faces = faceCascade.detectMultiScale(frame, 1.1, 3, 0, (10, 10))
            for (x, y, w, h) in faces:
                # Draw a green rectangle around the face (There is a lot of control to be had here, for example If you want a bigger border change 4 to 8)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
                self.object_x = x + (w/2)
                self.object_y = y + (h/2)
            time.sleep(0.1)
            frame = cv2.resize(frame, (540,300))
            frame = cv2.flip(frame, 1)
   
            # Display the video captured, with rectangles overlayed
            # onto the Pi desktop 
            cv2.imshow('Video', frame)

            #If you type q at any point this will end the loop and thus end the code.
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # When everything is done, release the capture information and stop everything
        video_capture.release()
        cv2.destroyAllWindows()

    def objectDetection(self,object,model):
        """
        Function for CV of any object, given a pre-trained model.
        object [str] = object to track, must be included in COCO file
        model [arr] = array of str paths to pre-trained model files. Including COCO names, config & weights files
        """

        classFile = model[0]
        with open(classFile,"rt") as f:
            classNames = f.read().rstrip("\n").split("\n")
            configPath = model[1]
            weightsPath = model[2]
        net = cv2.dnn_DetectionModel(weightsPath,configPath)
        net.setInputSize(self.screen[0],self.screen[1])
        net.setInputScale(1.0/ 127.5)
        net.setInputMean((127.5, 127.5, 127.5))
        net.setInputSwapRB(True)

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

            return img,objectInfo
        
        cap = cv2.VideoCapture(0)
        cap.set(3,self.screen[0])
        cap.set(4,self.screen[1])

        while True:
            success, img = cap.read()
            result, objectInfo = getObjects(img,0.2,0.2, objects=[object])
            time.sleep(0.1)
            if len(objectInfo) > 0:
                self.object_x = objectInfo[0][0][0] + int((objectInfo[0][0][2])/2)
                self.object_y = objectInfo[0][0][1] + int((objectInfo[0][0][3])/2)
                cv2.drawMarker(img,(self.object_x,self.object_y),color=(0,255,255),markerType = 0,markerSize = 10,thickness = 2)
                cv2.drawMarker(img,(320,240),color=(0,0,255),markerType=1,thickness=3)

            cv2.imshow("Output",img)
            cv2.waitKey(1)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # When everything is done, release the capture information and stop everything
        video_capture.release()
        cv2.destroyAllWindows()