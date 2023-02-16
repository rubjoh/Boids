

class Object:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def move(self):
        pass

    def get_box(self):
        return self.image.get_rect(topleft=(self.x, self.y))
