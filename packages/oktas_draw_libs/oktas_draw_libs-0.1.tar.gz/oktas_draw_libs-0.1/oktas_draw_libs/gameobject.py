from . import colors
class GameObject:
    def update(self, parent):
        pass

    def draw(self, parent):
        pass

    def fixed_update(self, parent):
        pass

class TestObject(GameObject):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velo = (0, 5)

    def draw(self, parent):
        parent.push()
        parent.translate(self.x + self.velo[0] * parent.interpolation, self.y + self.velo[1] * parent.interpolation)
        parent.rect(-50, -50, 100, 100)
        parent.fill = colors.BLUE
        parent.text_align_x = "CENTER"
        parent.text_align_y = "CENTER"
        parent.text("Test", 0, 0)
        parent.pop()

    def fixed_update(self, parent):
        self.x += self.velo[0]
        self.y += self.velo[1]

        if self.y > parent.height:
            self.y = -100
