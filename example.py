import pygame as p
import pymultiplayer as pmp

WIDTH = HEIGHT = 400
FPS = 60


def update(clock, buttons):
    for button in buttons:
        button.draw()

    clock.tick(FPS)
    p.display.update()


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("Multiplayer")
    clock = p.time.Clock()

    left_button = Button(0, 0, 200, 400, "Host a server", p.Color("grey 75"), screen, "left")
    right_button = Button(200, 0, 200, 400, "Join a server", p.Color("grey 25"), screen, "right")
    buttons = [left_button, right_button]

    running = True

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.x <= e.pos[0] <= (button.x + button.width) and button.y <= e.pos[1] <= (button.y + button.height):
                        button.clicked()

        update(clock, buttons)


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
        if self.id == "left":
            return "host"
        elif self.id == "right":
            return "join"


if __name__ == '__main__':
    main()
