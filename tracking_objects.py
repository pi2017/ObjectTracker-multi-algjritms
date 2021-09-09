#!/usr/bin/env python

import cv2


############### Tracker Types #####################

#tracker = cv2.TrackerBoosting_create()
# tracker = cv2.TrackerMIL_create()
# tracker = cv2.TrackerKCF_create()
# tracker = cv2.TrackerTLD_create()
# tracker = cv2.TrackerMedianFlow_create()
tracker = cv2.TrackerCSRT_create()
# tracker = cv2.TrackerMOSSE_create()

####################################################


print('Now type Start if you want to go back')
str1 = 'Start'
drawing = False
point = (0, 0)
rect_h = 45
rect_w = 45
event = True

while str1 == 'Start':

    cap = cv2.VideoCapture('d:/video/hd-demo.mp4')
    # TRACKER INITIALIZATION
    success, frame = cap.read()
    bbox = cv2.selectROI("Tracking", frame, False)
    tracker.init(frame, bbox)


    def mouse_drawing(event, x, y, flags, params):
        global point, drawing
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            x2 = x - int(rect_h / 2)
            y2 = y - int(rect_w / 2)
            point = (x2, y2)


    def drawBox(img, bbox):
         x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
         cv2.rectangle(img, (x, y), ((x + w), (y + h)), (255, 255, 0), 1, 1)
         cv2.putText(img, "Tracking", (100, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 1)

    while str1 == 'Start' :
        timer = cv2.getTickCount()
        success, img = cap.read()
        success, bbox = tracker.update(img)
        cv2.setMouseCallback("Tracking", mouse_drawing)


        if event == cv2.EVENT_LBUTTONDOWN:
            drawBox(img, bbox)
            cv2.rectangle(img, point, (point[0] + 80, point[1] + 80), (0, 0, 255), 0)
        else:
            cv2.putText(img, "Lost", (100, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1)
            pass

        cv2.rectangle(img, (15, 15), (200, 100), (255, 255, 0), 1)
        cv2.putText(img, "Fps:", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 1)
        cv2.putText(img, "Type:", (20, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 1)
        cv2.putText(img, "Status:", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 1)

        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
        if fps > 60:
            myColor = (250, 250, 0)
        elif fps > 20:
            myColor = (250, 250, 20)
        elif fps > 0:
            myColor = (250, 250, 30)
        else:
            myColor = (255, 250, 0)
        cv2.putText(img, str(int(fps)), (90, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, myColor, 1)
        cv2.imshow("Tracking", img)

        if cv2.waitKey(1) & 0xff == ord('q'):
            print('The End')
            cv2.destroyAllWindows()
            break
