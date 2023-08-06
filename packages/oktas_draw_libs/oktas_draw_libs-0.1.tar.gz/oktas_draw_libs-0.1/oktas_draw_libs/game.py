import pygame
from .layer import Layer
from . import colors

MS_PER_UPDATE = 50

class Game:
    #pylint: disable=R0902
    def __init__(self, *, caption="Some fancy Title", width=800, height=600, background_color=colors.LIGHT_GRAY):
        self.screen_size = (width, height)
        self.width = width
        self.height = height
        self.close_requested = False
        self.caption = caption
        self.surface = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()
        self.background_color = background_color
        self.loop = True
        self._lag = 0
        self.paused = False
        self.layers = [Layer()]

        self.events = {
            pygame.QUIT: self.quit,
            pygame.KEYDOWN: self.handle_keys,
            pygame.KEYUP: self.handle_keys
        }

        self.helperobject = HelperObject(self)

    @property
    def caption(self):
        return self._caption

    @caption.setter
    def caption(self, caption):
        # pylint: disable=W0201
        self._caption = caption
        pygame.display.set_caption(caption)

    def tick(self, fps):
        self.clock.tick(fps)

    def register_gameobject(self, game_object, layer_id=0):
        self.layers[layer_id].register_gameobject(game_object)

    def remove_gameobject(self, game_object, layer_id=0):
        self.layers[layer_id].remove_gameobject(game_object)

    def handle_events(self):
        for event in pygame.event.get():
            action = self.events.get(event.type)

            if action is not None:
                action(event)

    def quit(self, *_):
        self.close_requested = True

    def handle_keys(self, event):
        print(event)

    def update(self):

        if self.paused:
            return

        self.helperobject.delta = self.clock.get_time()
        self.helperobject.mouse_x, self.helperobject.mouse_y = pygame.mouse.get_pos()
        self._lag += self.helperobject.delta

        num_iterations = self._lag // MS_PER_UPDATE
        self._lag = self._lag % MS_PER_UPDATE

        for layer in self.layers:
            layer.update(self.helperobject, num_iterations)


    def draw(self):
        self.helperobject.reset_transforms()
        self.helperobject.interpolation = self._lag / MS_PER_UPDATE


        self.helperobject.background(self.background_color)

        for layer in self.layers:
            layer.draw(self.helperobject)

        pygame.display.update()


class HelperObject:
    def __init__(self, game):
        self.game = game
        self.stroke = colors.BLACK
        self.stroke_weight = 1
        self.text_align_x = "LEFT"
        self.text_align_y = "BOTTOM"
        self.text_size = 24
        self.fill = colors.WHITE
        self._no_fill = False
        self.transform_x = 0
        self.transform_y = 0
        self.rotation = 0,
        self._no_stroke = False
        self._stack = []
        self.delta = 0
        self.interpolation = 0
        self.mouse_x = 0
        self.mouse_y = 0

    @property
    def height(self):
        return self.game.height

    @property
    def width(self):
        return self.game.width

    @property
    def stroke(self):
        return self._stroke

    @stroke.setter
    def stroke(self, color):
        # pylint: disable=W0201
        if isinstance(color, str):
            self._stroke = pygame.Color(color)
        else:
            self._stroke = color
        self._no_stroke = False

    @property
    def fill(self):
        return self._fill

    @fill.setter
    def fill(self, color):
        # pylint: disable=W0201
        if isinstance(color, str):
            self._fill = pygame.Color(color)
        else:
            self._fill = color
        self._no_fill = False

    def simulate_updates(self, amount):
        self.game.simulate_updates(amount)

    def reset_transforms(self):
        self.transform_x = 0
        self.transform_y = 0
        self.rotation = 0
        self._stack = []

    def text(self, message, x, y):
        font = pygame.font.Font("Kenney Bold.ttf", self.text_size)
        surface = font.render(message, True, self.fill)
        rect = surface.get_rect()

        if self.text_align_x == "LEFT":
            rect.left = x + self.transform_x
        elif self.text_align_x == "CENTER":
            rect.centerx = x + self.transform_x
        else:
            rect.right = x + self.transform_x

        if self.text_align_y == "TOP":
            rect.top = y + self.transform_y
        elif self.text_align_y == "CENTER":
            rect.centery = y + self.transform_y
        else:
            rect.bottom = y + self.transform_y

        self.game.surface.blit(surface, rect)

    def push(self):
        self._stack.append((
            self.stroke,
            self.stroke_weight,
            self.text_align_x,
            self.text_align_y,
            self.text_size,
            self.fill,
            self.transform_x,
            self.transform_y,
            self.rotation,
            self._no_fill,
            self._no_stroke
        ))

    def pop(self):
        self.stroke, self.stroke_weight, self.text_align_x, self.text_align_y, self.text_size, \
        self.fill, self.transform_x, self.transform_y, self.rotation, self._no_fill, self._no_stroke = self._stack.pop()

    def translate(self, x, y):
        self.transform_x += x
        self.transform_y += y

    def rotate(self, angles):
        self.rotation += angles

    def arc(self, x, y, w, h, start_angle, stop_angle):
        if not self._no_stroke:
            pygame.draw.arc(
                self.game.surface,
                self.stroke,
                (x + self.transform_x, y + self.transform_y, w + self.transform_x, h + self.transform_y),
                start_angle,
                stop_angle,
                self.stroke_weight
            )

    def ellipse(self, x, y, w, h):
        if not self._no_fill:
            pygame.draw.ellipse(self.game.surface, self.fill, (x + self.transform_x, y + self.transform_y, w, h), 0)
        if not self._no_stroke:
            pygame.draw.ellipse(self.game.surface, self.stroke, (x + self.transform_x, y + self.transform_y, w, h), self.stroke_weight)

    def line(self, x1, y1, x2, y2):
        if not self._no_stroke:
            pygame.draw.line(
                self.game.surface,
                self.stroke,
                (x1 + self.transform_x, y1 + self.transform_y),
                (x2 + self.transform_x, y2 + self.transform_y),
                self.stroke_weight
            )

    def point(self, x, y):
        if not self._no_stroke:
            pygame.draw.circle(self.game.surface, self.stroke, (x + self.transform_x, y + self.transform_y), self.stroke_weight // 2)

    def rect(self, x, y, w, h):
        if not self._no_fill:
            pygame.draw.rect(self.game.surface, self.fill, (x + self.transform_x, y + self.transform_y, w, h))
        if not self._no_stroke:
            pygame.draw.rect(self.game.surface, self.stroke, (x + self.transform_x, y + self.transform_y, w, h), self.stroke_weight)

    def no_stroke(self):
        self._no_stroke = True

    def no_fill(self):
        self._no_fill = True

    def background(self, color):
        if isinstance(color, str):
            self.game.surface.fill(pygame.Color(color))
        else:
            self.game.surface.fill(color)
