#!/usr/bin/env python
"""
Use:
python objectdetector.py -v d:/video/hd-demo.mp4 -t csrt
or
python objectdetector.py -v d:/video/car-and-road.ts -t csrt
or
python objectdetector.py -v d:/video/road_bus.mp4 -t csrt
or
python objectdetector.py -v d:/video/pena_setka.mp4 -t csrt
or
python objectdetector.py -v d:/video/FlightTest/Video_2020_01_23_21_31_54.mp4 -t tld

Press "S" to stop stream and select ROI to tracking
Mouse left button select ROI than tap SPACE
Press "l" - to save image

Have a fun !!!
 """
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import datetime
import cv2
import sys
import time
import keyboard
import numpy as np

# this is required at the time of execution
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
                help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="csrt",
                help="OpenCV object tracker type")
args = vars(ap.parse_args())

OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.TrackerCSRT_create,
    "kcf": cv2.TrackerKCF_create,
    "boosting": cv2.TrackerBoosting_create,
    "mil": cv2.TrackerMIL_create,
    "tld": cv2.TrackerTLD_create,
    "medianflow": cv2.TrackerMedianFlow_create,
    "mosse": cv2.TrackerMOSSE_create
}
tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
print("tracker: ", args["tracker"])
initBB = None
success = None
key = cv2.waitKey(1) & 0xFF
drawing = False
point = (0, 0)
rect_h = 50
rect_w = 50


def mouse_drawing(event, x, y, flags, params):
    global point, drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        x2 = x - int(rect_h / 2)
        y2 = y - int(rect_w / 2)
        point = (x2, y2)


if not args.get("video", False):
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    time.sleep(1.0)

else:
    vs = cv2.VideoCapture(args["video"])

fps = None


def crosshair():
    # pts = np.array([[310, 230], [330, 230], [360, 230], [380, 230]], np.int32)
    # Creating a yellow polygon. Parameter "False" indicates
    # that our line is not closed
    # cv2.polylines(frame, [pts], False, (255, 255, 0), 2)

    cv2.line(frame, (310, 220), (330, 220), (255, 255, 0), 1)
    cv2.line(frame, (360, 220), (380, 220), (255, 255, 0), 1)
    cv2.line(frame, (345, 220), (345, 220), (255, 255, 0), 2)
    return crosshair


while True:

    frame = vs.read()
    frame = frame[1] if args.get("video", False) else frame
    if frame is None:
        print("No video")
        break

    frame = imutils.resize(frame, width=720)
    (H, W) = frame.shape[:2]
    if key == ord("s"):
        initBB = cv2.selectROI("Start Tracking", frame, showCrosshair=False, fromCenter=False)
        tracker.init(frame, initBB)
        fps = FPS().start()
        (success, box) = tracker.update(frame)
        cv2.setMouseCallback("Start Tracking", mouse_drawing)

    elif initBB is not None:
        # grab the new bounding box coordinates of the object
        (success, box) = tracker.update(frame)


        # check to see if the tracking was a success
        if success & drawing:
            cv2.rectangle(frame, point, (point[0] + rect_h, point[1] + rect_w), (0, 0, 255), 0)
            (x, y, w, h) = [int(v) for v in box]
            x2 = x - int(h / 2)
            y2 = y - int(w / 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h),
                          (255, 255, 250), 1)
            cv2.rectangle(frame, (x2, y2), (x2 + 2 * w, y2 + 2 * h),
                          (10, 10, 10), 1)
            cv2.putText(frame, args["tracker"], (x, y - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (36, 255, 12), 1)
        crosshair()
        # update the FPS counter
        fps.update()
        fps.stop()

        # initialize the set of information we'll be displaying on
        # the frame
        info = [
            ("Tracker", args["tracker"]),
            ("Success", "Yes" if success else "No"),
            ("FPS", "{:.2f}".format(fps.fps())),
        ]
        dt = str(datetime.datetime.now())
        # loop over the info tuples and draw them on our frame
        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            cv2.putText(frame, dt, (W - 315, H - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_8)

    # show the output frame
    cv2.imshow("Start Tracking", frame)
    key = cv2.waitKey(1) & 0xFF

    # if key == ord("s"):
    #     initBB = cv2.selectROI("Start Tracking", frame, showCrosshair=False, fromCenter=False)
    #     tracker.init(frame, initBB)
    #     fps = FPS().start()

    if key == ord("l"):
        initBB = cv2.selectROI("Start Tracking", frame, showCrosshair=True, fromCenter=False)
        imCrop = frame[int(initBB[1]):int(initBB[1] + initBB[3]), int(initBB[0]):int(initBB[0] + initBB[2])]
        cv2.imshow("Preview", imCrop)
        inname = time.strftime("%Y%m%d-%H%M%S")
        result = cv2.imwrite(r'static/preview-' + inname + '.png', imCrop)
        if result == True:
            print('File saved')
        else:
            print('Error saving file')
        fps = FPS().start()
        cv2.waitKey(1)  # ESC pressed

    elif key == ord('q'):
        print("Tracking stop by customer... ")
        break
