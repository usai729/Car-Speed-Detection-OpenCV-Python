import cv2 as cv
import time
import numpy as np

from tracker import *

car_detection_data = cv.CascadeClassifier("car_detection_data.xml")
object_detector = cv.createBackgroundSubtractorMOG2()
#Li165C-DN, cars-video_dBoddfSp_y1Sd
video = cv.VideoCapture("example_video_cars.mp4")
dist = 2.5
tracker = EuclideanDistTracker()
detections = []
crossed = set()
speed_rec = []

def check_append(id, crossedFunc=crossed):
    crossed.add(str(id))

while True:
    isTrue, frame = video.read()

    frame = cv.resize(frame, (900, 700), interpolation=cv.INTER_NEAREST)

    if isTrue:
        grayScale = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        grayScaleResized = cv.resize(grayScale, (400, 293), interpolation=cv.INTER_NEAREST)

        try:
            cv.putText(frame, f"Average speed: {int(sum(speed_rec)/len(speed_rec))}", (10, 100), cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), thickness=1)
        except ZeroDivisionError:
            pass

        cv.line(frame, (85, 150), (787, 150), (255, 0, 0), thickness=2)
        cv.line(frame, (75, 350), (777, 350), (0, 0, 255), thickness=2)

        cars = car_detection_data.detectMultiScale(grayScale, scaleFactor=1.3, minNeighbors=2)

        if len(cars) > 0:
            for (x, y, w, h) in cars:
                detections.append([x, y, w, h])

                cv.putText(frame, f"Live no. of cars detected: {len(cars)}", (10, 75), cv.FONT_HERSHEY_COMPLEX_SMALL, 1.2, (255, 255, 255), thickness=1)

                rectangled_img = cv.rectangle(frame, (x, y), (x+w, y+h), (0, 190, 200), thickness=2)

                if (y+h) >= 160:
                    time_i = time.time()
                    rectangled_img = cv.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), thickness=2)

                    boxes_ids = tracker.update(detections)

                    for i in boxes_ids:
                        x, y, w, h, id = i

                if (y+h) >= 360:
                    time_f = time.time()
                    check_append(id)

                    rectangled_img = cv.rectangle(frame, (x, y), (x+w, y+h), (0, 190, 200), thickness=2)

                    try:
                        speed = int((dist/(time_f-time_i))*3.6)
                        speed_rec.append(speed)

                        cv.putText(rectangled_img, f"{speed} KMPH", (x, y-15), cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), thickness=1)
                    except ZeroDivisionError:
                        cv.putText(rectangled_img, "N/A", (x, y-15), cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), thickness=1)

                cv.imshow("Frame", rectangled_img)
        else:
            cv.putText(frame, "No cars detected!", (10, 25), cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), thickness=2)
            
            cv.imshow("Frame", frame)
        cv.imshow("Video that is being processed", grayScaleResized)

        if cv.waitKey(1) & 0XFF==ord('d'):
            print(int(sum(speed_rec)/len(speed_rec)))
            break
    else:
        break

video.release()
cv.destroyAllWindows()
