from time import sleep

import pydirectinput

from core.input.input import InputWrapper


class DirectinputWrapper(InputWrapper):
    def __init__(self, interactions=True):
        self.with_interactions = interactions
        print("DirectinputWrapper initialized")

    def press(self, key):
        if not self.with_interactions:
            return
        pydirectinput.press(key)  # Simulate a key press
        print(f"Pressed key: {key}")

    def hold(self, key):
        if not self.with_interactions:
            return
        pydirectinput.keyDown(key)  # Simulate holding a key down
        print(f"Held key: {key}")

    def release(self, key):
        if not self.with_interactions:
            return
        pydirectinput.keyUp(key)  # Simulate releasing a key
        print(f"Released key: {key}")

    def move_to(self, x, y):
        if not self.with_interactions:
            return
        # Convert x and y to integers
        x = int(x)
        y = int(y)
        pydirectinput.moveTo(
            x, y, duration=0.5
        )  # Move the mouse to the specified coordinates
        print(f"Moved mouse to: ({x}, {y})")

    def left_click(self, x, y):
        if not self.with_interactions:
            return
        # Convert x and y to integers
        x = int(x)
        y = int(y)
        pydirectinput.click(x, y, duration=0.5, clicks=2)  # Simulate a left mouse click
        print(f"Left clicked at: ({x}, {y})")

    def right_click(self, x, y):
        if not self.with_interactions:
            return
        # Convert x and y to integers
        x = int(x)
        y = int(y)
        self.move_to(x, y)  # Move the mouse to the specified coordinates
        pydirectinput.click(button="right")  # Simulate a right mouse click
        print(f"Right clicked at: ({x}, {y})")

    def hold_and_move_to(self, x, y, distance):
        if not self.with_interactions:
            return
        # Convert x and y to integers
        x = int(x)
        y = int(y)
        self.move_to(x, y)  # Move the mouse to the starting position
        sleep(0.1)
        pydirectinput.mouseDown(button="right")  # Hold the right mouse button
        sleep(0.1)
        pydirectinput.moveTo(
            x + distance, y, duration=0.5
        )  # Move the mouse while holding the button
        sleep(0.1)
        pydirectinput.mouseUp(button="right")  # Release the right mouse button
        print(f"Held and moved to: ({x + distance}, {y})")
