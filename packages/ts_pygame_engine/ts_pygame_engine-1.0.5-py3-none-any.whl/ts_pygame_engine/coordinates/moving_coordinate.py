from ts_pygame_engine.primitives import Vector


class MovingCoordinate:
    def __init__(self, pos=(0, 0), vel=None, acc=None):
        self.pos = Vector(pos)
        self.vel = Vector(vel)
        self.acc = Vector(acc)

    def __str__(self):
        params = self.pos, self.vel, self.acc
        desc = '; '.join(str(round(z.x, 2)) + ',' + str(round(z.y, 2)) for z in params if z is not None)
        return '<MovingCoordinate %s>' % desc

    def process(self, game, time):
        self.vel += time * self.acc
        self.pos += time * self.vel

    @property
    def coords(self):
        return int(self.pos.x), int(self.pos.y)

    def debug_draw(self, screen, pygame, draw_acc=False):
        if draw_acc:
            start = self.pos
            end = start + self.acc
            color = (0, 255, 0)
            pygame.draw.line(screen, color, start.coords, end.coords, 2)
        start = self.pos
        end = start + self.vel
        color = (255, 0, 0)
        pygame.draw.line(screen, color, start.coords, end.coords, 2)
        color = (255, 255, 0)
        pygame.draw.circle(screen, color, self.coords, 2, 0)
