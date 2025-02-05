import cv2 as cv

TARGET_OFFSET = 10


class ComputerVision:

    def __init__(self):
        print("Computer Vision initialized")

    def find(self, img):
        # add black line for player nickname (center screen)
        centerX = int(img.shape[1] / 2) - 50
        centerY = int(img.shape[0] / 2) - 50

        # add black line for player nickname (center screen)
        img[centerY : centerY + 40, centerX : centerX + 100] = [0, 0, 0]
        # add black line for player hud (top screen)
        img[0:100, 0 : img.shape[1]] = [0, 0, 0]
        # add black line for player hud (bottom screen)
        img[img.shape[0] - 150 : img.shape[0], 0 : img.shape[1]] = [0, 0, 0]

        # converting screen to grayscale
        screen = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

        # finding white text (enemies)
        ret, enemies = cv.threshold(screen, 252, 255, cv.THRESH_BINARY)

        # forms a white bar in order to get the X and Y coordinates with the findContours and rectangle vision functions
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (50, 5))

        enemies = cv.morphologyEx(enemies, cv.MORPH_CLOSE, kernel)

        # cv.imshow("enemies", enemies)

        (contours, hierarchy) = cv.findContours(
            enemies, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE
        )

        # extracting enemy x and y coordinates from contours
        targets = []

        for c in contours:
            if cv.contourArea(c) > 50:
                x, y, w, h = cv.boundingRect(c)
                target = ((x + w / 2), (y + TARGET_OFFSET + h / 2))
                targets.append(target)

        return targets

    def draw_target_frames(self, img, targets, color=(0, 222, 0), thickness=2):
        for target in targets:
            cv.circle(img, (int(target[0]), int(target[1])), 10, color, thickness)

        return img
