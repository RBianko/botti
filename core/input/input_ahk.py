from ahk import AHK

from core.input.input import InputWrapper


class AhkInputWrapper(InputWrapper):
    def __init__(self, interactions=True):
        self.with_interactions = interactions
        self.ahk = AHK()
        print("AhkInputWrapper initialized")

    def press(self, key):
        if not self.with_interactions:
            return
        self.ahk.key_press(key)  # Simulate a key press
        print(f"Pressed key: {key}")

    def hold(self, key):
        if not self.with_interactions:
            return
        self.ahk.key_down(key)  # Simulate holding a key down
        print(f"Held key: {key}")

    def release(self, key):
        if not self.with_interactions:
            return
        self.ahk.key_up(key)  # Simulate releasing a key
        print(f"Released key: {key}")

    def move_to(self, x, y):
        if not self.with_interactions:
            return
        self.ahk.mouse_move(x, y)  # Move the mouse to the specified coordinates
        print(f"Moved mouse to: ({x}, {y})")

    def left_click(self, x, y):
        if not self.with_interactions:
            return
        self.ahk.mouse_move(x, y)  # Move the mouse to the specified coordinates
        self.ahk.click()  # Simulate a left mouse click
        print(f"Left clicked at: ({x}, {y})")

    def right_click(self, x, y):
        if not self.with_interactions:
            return
        self.ahk.mouse_move(x, y)  # Move the mouse to the specified coordinates
        self.ahk.click(button="right")  # Simulate a right mouse click
        print(f"Right clicked at: ({x}, {y})")

    def hold_and_move_to(self, x, y, distance):
        if not self.with_interactions:
            return
        self.ahk.mouse_move(x, y)  # Move the mouse to the starting position
        self.ahk.mouse_drag(
            x + distance, y, button="right", relative=False
        )  # Hold right button and drag
        print(f"Held and moved to: ({x + distance}, {y})")
