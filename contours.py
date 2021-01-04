import cv2

PIXELS_TO_MM = 0.2645833333

# Used to find contours (classify shapes)
def get_contours(img):
    # cv2.RETR_EXTERNAL good to find outer corners/details
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area_og = int(cv2.contourArea(cnt))
        if area_og > 50:
            # Outlines shapes in black
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            area = int(cv2.contourArea(cnt) * PIXELS_TO_MM)
            perimeter = int(cv2.arcLength(cnt, True) * PIXELS_TO_MM)
            # Calculates vertices
            approx_points = cv2.approxPolyDP(cnt, 0.02*(perimeter/PIXELS_TO_MM), True)
            object_corners = len(approx_points)
            # gives x, y, width and height of all shapes
            x, y, w, h = cv2.boundingRect(approx_points)

            # Determines shape based on vertices
            if object_corners > 7:
                objectType = "Circle"
            elif object_corners == 6:
                objectType = "Hexagon"
            elif object_corners == 4:
                aspRatio = w/float(h)
                if aspRatio > 0.9 and aspRatio < 1.2:
                    objectType = "Square"
                else:
                    objectType = "Rectangle"
            elif object_corners == 3:
                objectType = "Triangle"
            else:
                objectType = "TBD"

            # Outputs shape name, area and perimeter on image
            cv2.rectangle(imgContour, (x-5, y-5), (x+w+2, y+h+2), (0, 255, 0), 2)
            cv2.putText(imgContour, objectType,
                        (int(x+(w/2)-20), int(y+(h/2)-14)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.51, (0, 0, 0), 1)
            cv2.putText(imgContour, "A: " + str(area) + "mm",
                        (int(x+(w/2)-30), int(y+(h/2))), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (0, 0, 0), 1)
            cv2.putText(imgContour, "P: " + str(perimeter) + "mm",
                        (int(x+(w/2)-30), int(y+(h/2)+12)), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (0, 0, 0), 1)

path = "../Resources/shapes.png"
img = cv2.imread(path)
imgResize = cv2.resize(img, (500, 280))
imgContour = imgResize.copy()

imgGray = cv2.cvtColor(imgResize, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
imgCanny = cv2.Canny(imgBlur, 50, 50)
get_contours(imgCanny)

cv2.imshow("Contoured Image", imgContour)
cv2.waitKey(0)