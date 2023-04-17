import pygame as p
from button import Button
from constants import Constants

WIDTH = HEIGHT = 400
FPS = 60


def update(screen, clock, buttons, credit_text):
    for button in buttons:
        button.draw()

    credit_rect = credit_text.get_rect()
    credit_rect.center = (WIDTH / 2 - 2, HEIGHT - 20)
    screen.blit(credit_text, credit_rect)

    clock.tick(FPS)
    p.display.update()


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("Multiplayer")
    clock = p.time.Clock()

    credit_text = p.font.SysFont("verdana", 15).render("Multiplayer by: iamdeedz", True, p.Color("grey 50"))

    left_button = Button(0, 0, 200, 400, "Host a server", p.Color("grey 75"), screen, Constants.left)
    right_button = Button(200, 0, 200, 400, "Join a server", p.Color("grey 25"), screen, Constants.right)
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

        update(screen, clock, buttons, credit_text)


if __name__ == '__main__':
    main()
