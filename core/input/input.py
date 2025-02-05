from abc import ABC, abstractmethod


class InputWrapper(ABC):
    F1 = "f1"
    F2 = "f2"
    F3 = "f3"
    ESC = "esc"
    SHIFT = "shift"

    """ 
    Interface for input simulation classes.
    """

    @abstractmethod
    def press(self, key):
        """
        Simulate a key press.
        :param key: The key to press (e.g., 'f1', 'esc').
        """
        pass

    @abstractmethod
    def hold(self, key):
        """
        Simulate holding a key down.
        :param key: The key to hold (e.g., 'shift').
        """
        pass

    @abstractmethod
    def release(self, key):
        """
        Simulate releasing a key.
        :param key: The key to release (e.g., 'shift').
        """
        pass

    @abstractmethod
    def move_to(self, x, y):
        """
        Move the mouse to the specified coordinates.
        :param x: The x-coordinate.
        :param y: The y-coordinate.
        """
        pass

    @abstractmethod
    def left_click(self, x, y):
        """
        Simulate a left mouse click at the specified coordinates.
        :param x: The x-coordinate.
        :param y: The y-coordinate.
        """
        pass

    @abstractmethod
    def right_click(self, x, y):
        """
        Simulate a right mouse click at the specified coordinates.
        :param x: The x-coordinate.
        :param y: The y-coordinate.
        """
        pass

    @abstractmethod
    def hold_and_move_to(self, x, y, distance):
        """
        Hold the right mouse button and move the mouse by a specified distance.
        :param x: The starting x-coordinate.
        :param y: The starting y-coordinate.
        :param distance: The distance to move the mouse.
        """
        pass
