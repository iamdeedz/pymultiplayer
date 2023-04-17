import pygame as p
from constants import Constants


class Button:
    def __init__(self, x, y, width, height, text, colour, screen, id, font_size=25):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.colour = colour
        self.screen = screen
        self.id = id
        self.font_size = font_size
        self.font = p.font.SysFont("verdana", self.font_size)

    def draw(self):
        p.draw.rect(self.screen, self.colour, (self.x, self.y, self.width, self.height))
        text = self.font.render(self.text, True, p.Color("grey 50"))
        self.screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def clicked(self):
        if self.id == Constants.left:
            return Constants.host
        elif self.id == Constants.right:
            return Constants.join
