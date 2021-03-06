import numpy as np
import cv2
import time

windows = [(64, 128), (128, 128), (128, 64)]


def pyramid(image, scale=1.5, minSize=(20, 20)):
    # yield the original image
    # yield image

    # keep looping over the pyramid
    while True:
        # compute the new dimensions of the image and resize it
        w = int(image.shape[1] / scale)
        h = int(image.shape[0] / scale)
        image = cv2.resize(image, (w, h))  # imutils.resize(image, width=w)

        # if the resized image does not meet the supplied minimum
        # size, then stop constructing the pyramid
        if image.shape[0] < minSize[1] or image.shape[1] < minSize[0]:
            break

        # yield the next image in the pyramid
        yield image


def sliding_window(image, stepSize, windowSize):
    # slide a window across the image
    for y in xrange(0, image.shape[0], stepSize):
        for x in xrange(0, image.shape[1], stepSize):
            # yield the current window
            yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])


def capture():
    (winW, winH) = (256, 256)
    cap = cv2.VideoCapture(0)

    while(1):
        ret, frame = cap.read()

        # loop over the image pyramid
        for resized in pyramid(frame):
            # loop over the sliding window for each layer of the pyramid
            for (x, y, window) in sliding_window(resized, stepSize=32, windowSize=(winW, winH)):
                # if the window does not meet our desired window size, ignore
                # it
                if window.shape[0] != winH or window.shape[1] != winW:
                    continue

                # THIS IS WHERE YOU WOULD PROCESS YOUR WINDOW, SUCH AS APPLYING A
                # MACHINE LEARNING CLASSIFIER TO CLASSIFY THE CONTENTS OF THE
                # WINDOW

                # since we do not have a classifier, we'll just draw the window
                clone = resized.copy()
                cv2.rectangle(clone, (x, y), (x + winW,
                                              y + winH), (0, 255, 0), 2)
                cv2.imshow("Window", clone)
                cv2.waitKey(1)
                # time.sleep(0.025)

        cv2.imshow('SLIDING WINDOW', frame)

        if cv2.waitKey(30) & 0xff == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    capture()
