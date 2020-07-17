import cv2
import os
import pygame

#0 for cam, "*name*.mp4" for a premade recording
cap = cv2.VideoCapture(0);
found_eye = False

width = 0
height = 0

if cap.isOpened():
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))   # float
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float

#Create pygame
pygame.init()
pygame.display.set_caption("eye example")
screen = pygame.display.set_mode([width,height])

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

# now, to clear the screen
cls()

#nsize: 875, 575
fw1, fh1 = (267, 5)
fw2, fh2 = (1135, 559)


autoAdjust = False
customAdjust = False

useAutoAdjust = input("Use autoAdjust? 1 for yes, 0 for no: ") #auto adjust automatically adjusts to the eye when it tracks it
if useAutoAdjust == "1":
    autoAdjust = True
else:
    useCustomAdjust = input("Use customAdjust? 1 for yes, 0 for no: ") #custom adjust uses premade cords for the area where the eye should be
    if useCustomAdjust == "1":
        customAdjust = True
        fw1 = int(input("First x? Must be number: "))
        fh1 = int(input("First y? Must be number: "))
        fw2 = int(input("Second x? Must be number: "))
        fh2 = int(input("Second y? Must be number: "))


while True:
    ret, frame = cap.read()



    #roi = frame[269: 795, 537: 1416]
    if autoAdjust or customAdjust:
        roi= frame[fh1: fh2, fw1: fw2]
    else:
        roi = frame

    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray_roi = cv2.GaussianBlur(gray_roi, (7, 7), 0)

    rows, cols, _ = roi.shape

    _, threshold = cv2.threshold(gray_roi, 25, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

    blinking = False

    screen.fill((255, 255, 255))

    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)

        if w < 30 and h < 30:
            blinking = True
            break

        #more defined shape, what it's detecting
        cv2.drawContours(roi, [cnt], -3, (0, 0, 255), 3)

        #draw in grayscale
        cv2.drawContours(threshold, [cnt], -3, (125, 125, 125), 3)

        #rect around the eye
        cv2.rectangle(roi, (x, y), (x + w, y + h), (255, 0, 0), 2)

        #line to center of eye
        cv2.line(roi, (x + int(w/2), 0), (x + int(w/2), rows), (0, 255, 0), 2)
        cv2.line(roi, (0, y + int(h/2)), (cols, y + int(h/2)), (0, 255, 0), 2)

        #rect at center of eye
        x1, y1 = (x + int(w/2) - 1, y + int(h/2) - 1)
        x2, y2 = (x + int(w/2) + 1, y + int(h/2) + 1)
        cv2.rectangle(roi, (x1, y1), (x2, y2), (255, 0, 238), 2)

        #nsize: 875, 575
        cx, cy = (fw1 + x1 - 1, fh1 + y1 - 1)

        #change so the eye is in the center of the screen
        if autoAdjust:
            fw1, fh1 = (int(cx - (875/2) - 1), int(cy - (575/2) - 1))
            fw2, fh2 = (int(cx + (875/2) - 1), int(cy + (575/2) - 1))

        pygame.draw.circle(screen, (44, 201, 180), (x1 + 1, y1 + 1), 3)

        break

    if len(contours) == 0 or blinking:
        if found_eye:
            if blinking:
                cls()
                print("Eye might be blinking, alerting when eye has been found...")
            else:
                cls()
                print("No eye detected, alerting when detected.")
            found_eye = False

    else:
        if not found_eye:
            cls()
            print("Found eye, resuming...")
            found_eye = True


    cv2.imshow("filtered (threshold)", threshold)
    #cv2.imshow("gray roi", gray_roi) #removed, did not need window
    cv2.imshow("normal (roi)", roi)
    key = cv2.waitKey(1)
    if key == 27:
        break

    pygame.display.update()



cv2.destroyAllWindows()
