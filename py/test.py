import cv2 as cv
import numpy as np

img = cv.imread('triangle.png')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

edges = cv.Canny(gray, 50, 200)
contours, hierarchy = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    approx = cv.approxPolyDP(cnt, 0.01*cv.arcLength(cnt, True), True)
    if len(approx) == 3:
        score = cv.matchShapes(cnt, approx, cv.CONTOURS_MATCH_I1, 0)
        if score < 0.1:
            cv.drawContours(img, [cnt], 0, (0, 0, 255), 2)

cv.imshow('result', img)
cv.waitKey(0)
cv.destroyAllWindows()