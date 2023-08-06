from ts_pygame_engine.coordinates import MovingCoordinate


class Limit:
    def __init__(self, left, right):
        self.left = left
        self.right = right


class PosLimit:
    def __init__(self, x, y):
        self.x = Limit(*x)
        self.y = Limit(*y)


class LimitedMovingCoordinate(MovingCoordinate):
    def __init__(self, pos=(0, 0), vel=None, acc=None, limits=None, bounce=1):
        super().__init__(pos, vel, acc)
        self.limits = limits
        self.collision = False
        if bounce < 0:
            raise ValueError('bounce must be not negative number or bool')
        self.bounce = float(bounce)

    def process(self, game, time):
        super().process(game, time)
        if self.limits is None:
            return

        self.collision = False
        if self.pos.x < self.limits.x.left:
            self.pos.x = self.limits.x.left
            self.vel.x *= -self.bounce
            self.collision = True
        if self.pos.x > self.limits.x.right:
            self.pos.x = self.limits.x.right
            self.vel.x *= -self.bounce
            self.collision = True
        if self.pos.y < self.limits.y.left:
            self.pos.y = self.limits.y.left
            self.vel.y *= -self.bounce
            self.collision = True
        if self.pos.y > self.limits.y.right:
            self.pos.y = self.limits.y.right
            self.vel.y *= -self.bounce
            self.collision = True
