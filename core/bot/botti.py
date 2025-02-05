from enum import Enum
from time import time, sleep
from math import sqrt
import threading


class BotState(Enum):
    INITIALIZING = 0
    SEARCHING = 1
    TARGETING = 2
    ATTACKING = 3
    REBUFFING = 4


class Botti:

    # Settings
    init_seconds = 0

    # Properties
    state = None
    targets = []
    offset_x = 0
    offset_y = 0
    window_w = 0
    window_h = 0
    player_health = 100
    enemy_health = 0
    buffed = True
    message = ""

    input_wrapper = None

    player_class = None

    DEBUFF = None
    DAMAGE = None
    SUSTAIN = None
    TOGGLE = None

    def __init__(self, input_wrapper, offset_x, offset_y, w, h):
        print("Botti initialized")
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.window_w = w
        self.window_h = h

        self.state = BotState.INITIALIZING

        self.input_wrapper = input_wrapper

        self.DEBUFF = self.input_wrapper.F1
        self.DAMAGE = self.input_wrapper.F2
        self.SUSTAIN = self.input_wrapper.F3

        # Threading
        self.bot_thread_stop_event = threading.Event()
        self.bot_thread = threading.Thread(target=self.bot_loop)

        self.timestamp = time()

    def bot_loop(self):
        while not self.bot_thread_stop_event.is_set():
            if self.state == BotState.INITIALIZING:
                self.message = "STARTING!"
                self.state = BotState.SEARCHING

            elif self.state == BotState.SEARCHING:
                self.message = "Looking for enemies"
                if self.targets is not None and len(self.targets) > 0:
                    self.timestamp = time()
                    self.state = BotState.TARGETING
                else:
                    self.message = "No enemies found. Turning camera"
                    sleep(0.5)
                    self.turn_camera()
                    sleep(0.5)

            elif self.state == BotState.TARGETING:
                self.message = "Trying to target enemies"
                if self.target():
                    self.state = BotState.ATTACKING

            elif self.state == BotState.ATTACKING:
                self.message = "ATTACKING"
                if not self.attack():
                    self.state = BotState.SEARCHING

            elif self.state == BotState.REBUFFING:
                if self.buffed:
                    self.state = BotState.SEARCHING
                else:
                    pass

            sleep(0.5)

    def target(self):
        if self.state is BotState.TARGETING:
            return False

        target_i = 0
        targets = self.target_sorting(self.targets)

        while target_i < len(targets):
            self.state = BotState.TARGETING
            x, y = self.get_screen_position(targets[target_i])

            self.try_target(x, y)
            if self.enemy_health is not None and self.enemy_health > 0:
                return True
            self.try_target(x, y + 10)
            if self.enemy_health is not None and self.enemy_health > 0:
                return True
            self.try_target(x, y + 20)
            if self.enemy_health is not None and self.enemy_health > 0:
                return True
            self.try_target(x, y + 30)
            if self.enemy_health is not None and self.enemy_health > 0:
                return True
            self.try_target(x, y + 40)
            if self.enemy_health is not None and self.enemy_health > 0:
                return True

            target_i += 1

        self.state = BotState.SEARCHING
        return False

    def try_target(self, x, y):
        self.keyboard_event(self.input_wrapper.SHIFT, hold=True)
        sleep(0.5)
        self.mouse_click(x, y)
        sleep(0.5)
        self.keyboard_event(self.input_wrapper.SHIFT, release=True)

    def attack(self):
        if (time() - self.timestamp) > 15:
            sleep(0.5)
            self.keyboard_event(self.input_wrapper.ESC)
            sleep(0.5)
            return False

        if self.enemy_health is None:
            return False

        elif self.enemy_health == 0:
            sleep(0.5)
            self.keyboard_event(self.input_wrapper.ESC)
            sleep(0.5)
            # Try next target
            return False

        elif self.player_health <= 40 and self.enemy_health > 0:
            self.timestamp = time()
            sleep(0.5)
            ability = self.SUSTAIN
            self.keyboard_event(ability)
            sleep(0.5)

        elif self.player_health > 70 and self.enemy_health > 0:
            self.timestamp = time()
            ability = self.DAMAGE
            sleep(0.5)
            self.keyboard_event(ability)
            sleep(0.5)

        return True

    def keyboard_event(self, key, hold=False, release=False):
        if not hold and not release:
            self.input_wrapper.press(key)
        elif hold:
            self.input_wrapper.hold(key)
        elif release:
            self.input_wrapper.release(key)

    def mouse_click(self, x, y, left=True):
        if left:
            self.input_wrapper.left_click(x, y)
        else:
            self.input_wrapper.right_click(x, y)

    def drag_camera(self, x, y, distance):
        self.input_wrapper.hold_and_move_to(x, y, distance)

    def target_sorting(self, targets):
        my_pos = (self.window_w / 2, self.window_h / 2)

        def pythagorean_distance(pos):
            return sqrt(
                (float(pos[0]) - my_pos[0]) ** 2 + (float(pos[1]) - my_pos[1]) ** 2
            )

        targets.sort(key=pythagorean_distance)

        # Remove targets that are further away than SEARCH_RADIUS
        targets = [t for t in targets if pythagorean_distance(t) > 100]

        return targets

    def turn_camera(self):
        print("Turning camera")
        x = self.offset_x + self.window_w / 2
        y = self.offset_y + self.window_h / 2

        self.drag_camera(x, y, 10)

    def get_screen_position(self, pos):
        return pos[0] + self.offset_x, pos[1] + self.offset_y

    def update_targets(self, targets):
        self.targets = targets

    def update_hp(self, player, enemy):
        self.enemy_health = enemy
        self.player_health = player

    def stop(self):
        self.bot_thread_stop_event.set()
        self.bot_thread.join()

    def start(self):
        self.bot_thread.start()
