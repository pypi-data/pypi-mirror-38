from ts_pygame_engine.coordinates.limited_moving_coordinate import LimitedMovingCoordinate
from ts_pygame_engine.primitives import Vector


class SlowingCoordinate(LimitedMovingCoordinate):
    def __init__(self, pos=(0, 0), vel=None, acc=None, limits=None, bounce=False, slowing_speed=None):
        super().__init__(pos, vel, acc, limits, bounce)
        self.slowing = True
        if type(slowing_speed) in [int, float]:
            self.slowing_speed = Vector(slowing_speed, slowing_speed)
        elif slowing_speed is None:
            self.slowing_speed = Vector()
        else:
            self.slowing_speed = slowing_speed

    def process(self, game, time):
        super().process(game, time)
        if not self.slowing:
            return
        if self.vel.x != 0 and self.acc.x == 0:
            self.vel.x *= self.slowing_speed.x ** time
            if abs(self.vel.x) <= 0.01:
                self.vel.x = 0
        if self.vel.y != 0 and self.acc.y == 0:
            self.vel.y *= self.slowing_speed.y ** time
            if abs(self.vel.y) <= 0.01:
                self.vel.y = 0

