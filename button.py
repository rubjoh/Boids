import pygame

class ToggleButton:
    def __init__(self, x, y, width, height, on_text, off_text, font, on_color, off_color, screen, initial_state=True):
        self.rect = pygame.Rect(x, y, width, height)
        self.on_text = on_text
        self.off_text = off_text
        self.font = font
        self.on_color = on_color
        self.off_color = off_color
        self.screen = screen
        self.state = initial_state

    def draw(self):
        '''Drawing the toggle buttons on screen'''
        if self.state == True:
            color = self.on_color
        else: 
            color = self.off_color

        if self.state == True:
            text = self.on_text
        else: 
            text = self.off_text

        surface = self.font.render(text, True, color)
        self.screen.blit(surface, (self.rect.x, self.rect.y))

    def check_clicked(self, event, pos):
        '''Checks if the button is clicked'''
        if event.type == pygame.MOUSEBUTTONUP and self.rect.collidepoint(pos):
            self.state = not self.state
            return True
        return False
