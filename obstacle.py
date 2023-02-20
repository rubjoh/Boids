from objects import Object

class Obstacle(Object):
    def __init__(self, x, y, image, screen_width, screen_height):
        super().__init__(x, y, image, screen_width, screen_height)

    def update(self):
        # Obstacles do not move
        pass

    


    




