#!/usr/bin/env python

'''
Using Correlation Trackers in Dlib, you can track any object in a video stream without
needing to train a custom object detector.

Click leftbutton and hold to select object.
When you will see yellow rectangle push "t"
Cancel tracking push "r"
'''

import numpy as np
import cv2
import dlib
import datetime
import imutils
import numpy as np

rect_h = 50
rect_w = 50

markers = [
    cv2.MARKER_CROSS,
    # cv2.MARKER_TILTED_CROSS,
    # cv2.MARKER_STAR,
    # cv2.MARKER_DIAMOND,
    # cv2.MARKER_SQUARE,
    # cv2.MARKER_TRIANGLE_UP,
    # cv2.MARKER_TRIANGLE_DOWN
]

def draw_border(img, pt1, pt2, color, thickness, r, d):
    x1, y1 = pt1
    x2, y2 = pt2
    # Top left
    cv2.line(img, (x1 + r, y1), (x1 + r + d, y1), color, thickness)
    cv2.line(img, (x1, y1 + r), (x1, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)
    # Top right
    cv2.line(img, (x2 - r, y1), (x2 - r - d, y1), color, thickness)
    cv2.line(img, (x2, y1 + r), (x2, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)
    # Bottom left
    cv2.line(img, (x1 + r, y2), (x1 + r + d, y2), color, thickness)
    cv2.line(img, (x1, y2 - r), (x1, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)
    # Bottom right
    cv2.line(img, (x2 - r, y2), (x2 - r - d, y2), color, thickness)
    cv2.line(img, (x2, y2 - r), (x2, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)

def crosshair():
    # pts = np.array([[310, 230], [330, 230], [360, 230], [380, 230]], np.int32)
    # Creating a yellow polygon. Parameter "False" indicates
    # that our line is not closed
    # cv2.polylines(frame, [pts], False, (255, 255, 0), 2)

    cv2.line(frame, (310, 220), (330, 220), (255, 255, 0), 1)
    cv2.line(frame, (360, 220), (380, 220), (255, 255, 0), 1)
    cv2.line(frame, (345, 220), (345, 220), (255, 255, 0), 2)
    return crosshair


# this variable will hold the coordinates of the mouse click events.
mousePoints = []


def mouseEventHandler(event, x, y, flags, param):
    # references to the global mousePoints variable
    global mousePoints

    # if the left mouse button was clicked, record the starting coordinates.
    if event == cv2.EVENT_LBUTTONDOWN:
        mousePoints = [(x, y)]

    # when the left mouse button is released, record the ending coordinates.
    elif event == cv2.EVENT_LBUTTONUP:
        mousePoints.append((x, y))


# create the video capture.
video_capture = cv2.VideoCapture('d:/video/hd-demo.mp4')
#video_capture = cv2.VideoCapture('d:/video/aeropract/aero-hd.m2ts')
#video_capture = cv2.VideoCapture('d:/video/hd-demo.mp4')


# create a named window in OpenCV and attach the mouse event handler to it.
cv2.namedWindow("Video stream")
cv2.setMouseCallback("Video stream", mouseEventHandler)

# initialize the correlation tracker.
tracker = dlib.correlation_tracker()

# this is the variable indicating whether to track the object or not.
tracked = False

while True:
    # start capturing the video stream.
    ret, frame = video_capture.read()
    frame = imutils.resize(frame, width=1080)
    (H, W) = frame.shape[:2]
    if ret:
        image = frame


        # if we have two sets of coordinates from the mouse event, draw a rectangle.
        if len(mousePoints) == 2:
            cv2.rectangle(image, mousePoints[0], mousePoints[1], (255, 255, 255), 1)
            dlib_rect = dlib.rectangle(mousePoints[0][0], mousePoints[0][1], mousePoints[1][0], mousePoints[1][1])

        # tracking in progress, update the correlation tracker and get the object position.
        if tracked == True:
            tracker.update(image)
            track_rect = tracker.get_position()
            x = int(track_rect.left())
            y = int(track_rect.top())
            x1 = int(track_rect.right())
            y1 = int(track_rect.bottom())



            # Draw rectangle for target
            #cv2.rectangle(image, (x, y), (x1, y1), (0, 0, 255), 1)  # red tracker marker
            cv2.putText(frame, "TARGET", (x - 4, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1, cv2.LINE_8)
            # Draw crosshair for target
            draw_border(image, (x, y), (x1, y1), (127, 255, 255), 1, 3, 9)

        # show the current frame.
        dt = str(datetime.datetime.now())
        cv2.putText(frame, dt, (W - 230, H - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_8)
        cv2.putText(frame, "Hold LButton to select target", (W - 700, H - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.38,
                    (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, "Press 't' to tracking", (W - 700, H - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.38,
                    (255, 255, 255), 1, cv2.LINE_AA)
        cv2.imshow("Video stream", image)

    # capture the keyboard event in the OpenCV window.
    ch = 0xFF & cv2.waitKey(1)

    # press "r" to stop tracking and reset the points.
    if ch == ord("r"):
        mousePoints = []
        tracked = False

    # press "t" to start tracking the currently selected object/area.
    if ch == ord("t"):
        if len(mousePoints) == 2:
            tracker.start_track(image, dlib_rect)
            tracked = True
            mousePoints = []

    # press "q" to quit the program.
    if ch == ord('q'):
        break

# cleanup windows
print('The End')
video_capture.release()
cv2.destroyAllWindows()
