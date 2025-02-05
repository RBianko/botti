import threading
from time import sleep

import cv2 as cv
import keyboard

from core.bot.botti import Botti
from core.config_parser import ConfigParser
from core.input.input_ahk import AhkInputWrapper
from core.input.input_pydirectinput import DirectinputWrapper
from core.vision.computer_vision import ComputerVision
from core.vision.vision_helper import VisionHelper
from core.vision.window_capture import WindowCapture


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Launcher:
    __metaclass__ = Singleton

    vision = None
    vision_helper = None
    window_capture = None
    bot = None
    config = None

    def __init__(self):
        print("MAIN: INIT!")
        self.config = ConfigParser()

        self.bot_thread_stop_event = threading.Event()
        self.bot_thread = threading.Thread()

        self.vision_thread = threading.Thread(target=self.start_vision)

        keyboard.add_hotkey("ctrl+w", self.start_bot)
        keyboard.add_hotkey("ctrl+q", self.stop_bot)
        print("CTRL + W to START BOT")

        self.vision_thread.start()

    def start_vision(self):
        print("MAIN: START VISION: IS DEBUG: {}".format(self.config.is_debug))
        message: str = ""

        # Wait for window_capture to be initialized
        while self.window_capture is None:
            try:
                self.window_capture = WindowCapture(self.config.window_name)
            except Exception as e:
                self.window_capture = None
                print(e)
            sleep(1)

        self.vision = ComputerVision()
        self.vision_helper = VisionHelper(
            self.window_capture.w,
            self.window_capture.h,
            self.config.ui_info_path,
        )

        while True:
            snapshot = self.window_capture.capture()

            # Check if snapshot is valid
            if snapshot is None or snapshot.size == 0:
                print("ERROR: Invalid snapshot. Skipping frame.")
                continue

            # Get player and enemy health
            self.vision_helper.get_hp(snapshot)

            # Get targets
            objects = self.vision.find(snapshot)

            if self.config.is_debug:
                view = self.vision.draw_target_frames(snapshot, objects)
                view = self.vision_helper.draw_ui_positions(
                    view, self.window_capture.fps
                )

                # Check if view is valid
                if view is None or view.size == 0:
                    print("ERROR: Invalid view. Skipping frame.")
                    continue

                if self.bot is not None:
                    view = self.vision_helper.draw_bot_info(view, self.bot)

                try:
                    cv.imshow("ComputerVision", view)
                except cv.error as e:
                    print(f"ERROR: Failed to display view: {e}")

            if self.bot is not None:
                self.bot.update_targets(objects)
                self.bot.update_hp(
                    self.vision_helper.current_player_health,
                    self.vision_helper.current_enemy_health,
                )

                if message is not self.bot.message:
                    print(self.bot.message)
                    message = self.bot.message

            if cv.waitKey(1) & 0xFF == ord("q"):
                break

    def start_bot(self):
        print("MAIN: START BOT in 3 seconds")
        sleep(3)

        input_wrapper = DirectinputWrapper()
        self.bot = Botti(
            input_wrapper,
            self.window_capture.offset_x + self.window_capture.cropped_x,
            self.window_capture.offset_y + self.window_capture.cropped_y,
            self.window_capture.w,
            self.window_capture.h,
        )
        self.bot.start()

    def stop_bot(self):
        print("MAIN: STOP BOT!")
        self.bot.stop()
        self.bot_thread_stop_event.set()
        self.bot = None
