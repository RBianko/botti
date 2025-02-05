import configparser
from time import time, sleep

import cv2 as cv
import numpy as np
import pytesseract
from PIL import Image, ImageFilter, ImageEnhance


class VisionHelper:
    timestamp = 0

    current_player_health = 100  # %
    current_enemy_health = 100  # %

    player_hp_x_pos = 0
    player_hp_y_pos = 0
    player_hp_bar_width = 0
    player_hp_bar_height = 0
    enemy_hp_x_pos = 0
    enemy_hp_y_pos = 0
    enemy_hp_bar_width = 0
    enemy_hp_bar_height = 0

    font = cv.FONT_HERSHEY_COMPLEX_SMALL

    def __init__(self, w, h, ui_info):
        print("Helper initialized")
        self.w = w
        self.h = h

        self.get_ui_positions(ui_info)

    def get_ui_positions(self, ui_info):
        config = configparser.ConfigParser()
        config.read(ui_info)

        status_wnd = "StatusWnd"

        self.player_hp_x_pos = config.getint(status_wnd, "x") + 50
        self.player_hp_y_pos = config.getint(status_wnd, "y") + 20
        self.player_hp_bar_width = 180
        self.player_hp_bar_height = 25

        self.enemy_hp_x_pos = self.player_hp_x_pos + self.player_hp_bar_width + 30
        self.enemy_hp_y_pos = self.player_hp_y_pos + 10
        self.enemy_hp_bar_width = 160
        self.enemy_hp_bar_height = 15

    def get_hp(self, img):
        # update every 1.5 seconds
        if time() - self.timestamp > 1.5:
            self.timestamp = time()

            # get player health
            y_player = self.player_hp_y_pos
            h_player = self.player_hp_bar_height + y_player
            x_player = self.player_hp_x_pos
            w_player = self.player_hp_bar_width + x_player
            frame_player = img[y_player:h_player, x_player:w_player]
            # cv.imshow("frame_player", frame_player)
            self.current_player_health = self.get_hp_by_color(frame_player)
            self.analyze_hsv_values(frame_player)
            self.debug_hp_parsing(frame_player, "Player HP")

            y_enemy = self.enemy_hp_y_pos
            h_enemy = self.enemy_hp_bar_height + y_enemy
            x_enemy = self.enemy_hp_x_pos
            w_enemy = self.enemy_hp_bar_width + x_enemy
            frame_enemy = img[y_enemy:h_enemy, x_enemy:w_enemy]
            # cv.imshow("frame_enemy", frame_enemy)
            self.current_enemy_health = self.get_hp_by_color(frame_enemy)
            self.analyze_hsv_values(frame_enemy)
            self.debug_hp_parsing(frame_enemy, "Enemy HP")

    def get_hp_text(self, hp_region):
        # Perform text extraction
        gray = cv.cvtColor(hp_region, cv.COLOR_BGR2GRAY)
        ret, thresh1 = cv.threshold(gray, 0, 255, cv.THRESH_OTSU | cv.THRESH_BINARY_INV)

        data = pytesseract.image_to_string(
            thresh1,
            lang="eng",
            config="-c tessedit_char_whitelist=0123456789/",
        )

        try:
            currentHp = int(data.split("/")[0])
            maxHp = int(data.split("/")[1])
            return int((currentHp / maxHp) * 100)
        except (ValueError, IndexError):
            return None

    def get_hp_by_color(self, hp_region):
        """
        Parse HP percentage by detecting the red color in the HP bar, ignoring text and dark pixels.
        :param hp_region: Cropped image of the HP bar (in BGR format).
        :return: HP percentage (0-100) or None if parsing fails.
        """

        # Convert the image to HSV color space
        hsv = cv.cvtColor(hp_region, cv.COLOR_BGR2HSV)

        # Define the range of red color in HSV
        lower_red1 = np.array([0, 50, 50])  # Lower bound for red (0-10)
        upper_red1 = np.array([10, 255, 255])  # Upper bound for red (0-10)
        lower_red2 = np.array([170, 50, 50])  # Lower bound for red (170-180)
        upper_red2 = np.array([180, 255, 255])  # Upper bound for red (170-180)

        # Create masks for the two red ranges
        mask1 = cv.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv.inRange(hsv, lower_red2, upper_red2)

        # Combine the masks
        red_mask = cv.bitwise_or(mask1, mask2)

        # Remove dark pixels (text and shadows) from the mask
        value_mask = cv.inRange(
            hsv, np.array([0, 0, 50]), np.array([180, 255, 255])
        )  # Exclude pixels with V < 50
        red_mask = cv.bitwise_and(red_mask, value_mask)

        # Calculate the number of red pixels (ignoring text and dark pixels)
        red_pixels = np.sum(red_mask > 0)

        # Calculate the total number of pixels in the HP bar (ignoring text and dark pixels)
        total_pixels = np.sum(value_mask > 0)

        # Calculate the HP percentage
        if total_pixels > 0:
            hp_percentage = (red_pixels / total_pixels) * 100
            return int(hp_percentage)
        else:
            return None

    def debug_hp_parsing(self, hp_region, region_name):
        """
        Debug HP parsing by displaying the red mask and HP region.
        :param hp_region: Cropped image of the HP bar.
        :param region_name: Name of the region (e.g., "Player HP" or "Enemy HP").
        """
        # Convert the image to HSV color space
        hsv = cv.cvtColor(hp_region, cv.COLOR_BGR2HSV)

        # Define the range of red color in HSV
        lower_red1 = np.array([0, 50, 50])  # Lower bound for red (0-10)
        upper_red1 = np.array([10, 255, 255])  # Upper bound for red (0-10)
        lower_red2 = np.array([170, 50, 50])  # Lower bound for red (170-180)
        upper_red2 = np.array([180, 255, 255])  # Upper bound for red (170-180)

        # Create masks for the two red ranges
        mask1 = cv.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv.inRange(hsv, lower_red2, upper_red2)

        # Combine the masks
        red_mask = cv.bitwise_or(mask1, mask2)

        # Remove dark pixels (text and shadows) from the mask
        value_mask = cv.inRange(
            hsv, np.array([0, 0, 50]), np.array([180, 255, 255])
        )  # Exclude pixels with V < 50
        red_mask = cv.bitwise_and(red_mask, value_mask)

        # Display the original HP region, red mask, and value mask
        cv.imshow(f"{region_name} Region", hp_region)
        cv.imshow(f"{region_name} Red Mask", red_mask)
        cv.imshow(f"{region_name} Value Mask", value_mask)
        cv.waitKey(1)

    def draw_ui_positions(self, view, fps):
        view = cv.putText(
            view,
            f"Player HP: {self.current_player_health}%",
            (15, 140),
            self.font,
            0.8,
            (155, 222, 155),
            1,
            cv.LINE_AA,
        )
        view = cv.putText(
            view,
            f"Target HP: {self.current_enemy_health}%",
            (15, 160),
            self.font,
            0.8,
            (155, 155, 222),
            1,
            cv.LINE_AA,
        )
        view = cv.putText(
            view,
            f"FPS: {int(fps)}",
            (15, 120),
            self.font,
            0.8,
            (155, 155, 155),
            1,
            cv.LINE_AA,
        )

        return view

    def analyze_hsv_values(self, hp_region):
        """
        Analyze the HSV values of the HP bar to determine the correct red color range.
        :param hp_region: Cropped image of the HP bar (in BGR format).
        """
        # Convert the image to HSV color space
        hsv = cv.cvtColor(hp_region, cv.COLOR_BGR2HSV)

        # Flatten the HSV array to get all pixel values
        hsv_values = hsv.reshape(-1, 3)

        # Print the min and max HSV values
        print("Min HSV values:", np.min(hsv_values, axis=0))
        print("Max HSV values:", np.max(hsv_values, axis=0))

    def draw_bot_info(self, view, bot):
        view = cv.putText(
            view,
            f"State: {bot.state.name}",
            (15, 180),
            self.font,
            0.8,
            (155, 255, 155),
            1,
            cv.LINE_AA,
        )
        view = cv.putText(
            view,
            f"Message: {bot.message}",
            (15, 210),
            self.font,
            0.8,
            (155, 255, 155),
            1,
            cv.LINE_AA,
        )
        view = cv.putText(
            view,
            f"Target: {bot.targets}",
            (15, 230),
            self.font,
            0.6,
            (155, 255, 155),
            1,
            cv.LINE_AA,
        )

        return view
