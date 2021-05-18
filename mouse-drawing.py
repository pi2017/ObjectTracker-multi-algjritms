#!/usr/bin/env python

import numpy as np
import cv2

drawing = False
point = (0, 0)

"""
def mouse_drawing(event, x, y, flags, params):
    global point, drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        point = (x, y)
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing is True:
            point = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        point = (x, y)
"""

def mouse_drawing(event, x, y, flags, params):
    global point, drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        point = (x, y)


cap = cv2.VideoCapture('d:/video/road_bus.mp4')
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", mouse_drawing)

while True:
    _, frame = cap.read()
    if drawing:
        cv2.rectangle(frame, point, (point[0] + 80, point[1] + 80), (0, 0, 255), 0)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(25)
    if key == 13:
        print('done')
    elif key == 27:
        break

cap.release()
cv2.destroyAllWindows()
