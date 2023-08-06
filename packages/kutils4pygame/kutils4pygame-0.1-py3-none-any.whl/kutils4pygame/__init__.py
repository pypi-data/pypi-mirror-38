"""Classes for creating game with display and animation."""
from pygame import display, time, event, Rect, Surface, QUIT
import sys


class EmptyAnimation(Exception):
    """Exception raised when attempting to construct an empty animation."""

    def __init__(self):
        """Empty constructor."""
        pass


class Game(object):
    """Object for game, runs game loop and contains screen."""

    def __init__(self, screen_w, screen_h, fps):
        """Initialize display and clock for game object."""
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.display = Display(screen_w, screen_h)
        self.clock = time.Clock()
        self.event_dict = {}
        self.fps = fps

    def quit(self):
        """Quit game and destroy display."""
        quit()
        sys.exit()

    def start(self):
        """Initiate game loop."""
        while True:
            for e in event.get():
                if e.type == QUIT:
                    self.quit()

            self.run()
            display.update()
            self.clock.tick(self.fps)

    def run(self):
        """Dummy run definition."""
        old_values = list(self.display.board.values())
        Animation.animate_iterable(old_values, self.display)


class Display(object):
    """Object representing display."""

    def __init__(self, screen_w, screen_h, bgrnd=None, bgrnd_x=0, bgrnd_y=0):
        """Init display."""
        self.display = display.set_mode((screen_w, screen_h))
        self.board = {}
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.background = bgrnd

        if self.background:
            self.display.blit(self.background, (bgrnd_x, bgrnd_y))

    def background_sub(self, x, y, w, h):
        """Get subsurface of background."""
        if self.background:
            return self.background.subsurface(Rect(x, y, w, h))
        s = Surface((w, h))
        s.fill((0, 0, 0))
        return s

    def blit(self, animation):
        """Blit animation at animation's x,y and add animation to objects."""
        x = animation.x
        y = animation.y
        self.blit_background(animation)
        self.display.blit(animation.get_image(), (x, y))

    def blit_background(self, animation):
        """Blit subsurface of background over animation's rect."""
        x = animation.x
        y = animation.y
        w = animation.w
        h = animation.h
        bground = self.background_sub(x, y, w, h)
        self.display.blit(bground, (x, y))

    def kill(self, animation):
        """Remove animation from board and blit background overtop."""
        x = animation.x
        y = animation.y
        self.blit_background(animation)
        del self.board[(x, y)]


class Animation(object):
    """Animation class for blitting series of images at certain rate."""

    @staticmethod
    def animate_iterable(iterable, surface):
        """Blit given iterable on screen."""
        for i in iterable:
            i.animate(surface)

    @staticmethod
    def move_iterable(iterable, surface):
        """Move all vals of given iterable within screen."""
        for i in iterable:
            i.move(surface)

    def __init__(self, x, y, w, h, fpi=1, delay=0, iterable=[]):
        """Initialize Animation instance."""
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.fpi = fpi
        self.frames_since_animate = fpi - delay - 1
        self.images = iterable
        self.images_iterator = iter(self.images)
        self.is_dead = False
        self.dying = False

    def animate(self, display):
        """Blit current image on surface after blitting background."""
        self.degrade()
        self.frames_since_animate += 1
        if self.frames_since_animate >= self.fpi:
            if not self.dead():
                display.blit(self)
                self.move()
                self.frames_since_animate = 0
            else:
                self.die(display)

    def get_image(self):
        """Get next image in sequence (start over if none left)."""
        if not self.images:
            raise EmptyAnimation
        try:
            r = next(self.image_iterator)
        except StopIteration:
            self.image_iterator = iter(self.images)
            r = next(self.image_iterator)

        return r

    def die(self, display):
        """Die and delete self from display."""
        display.kill(self)

    def dead(self):
        """Empty for updating and returning dead status."""
        return self.is_dead

    def move(self):
        """Empty update children."""
        pass

    def degrade(self):
        """Bring Animation closer to death."""
        pass
