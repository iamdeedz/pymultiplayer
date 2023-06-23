import pymultiplayer as pmp
import pygame as p


def msg_received(msg):
    print(f"Server sent message: {msg}")


def loop(*args):
    p.init()
    fps = 60
    client = args[0]
    screen = p.display.set_mode((500, 500))
    p.display.set_caption("Test Client")
    clock = p.time.Clock()
    while True:
        for e in p.event.get():
            if e.type == p.QUIT:
                client.disconnect()
                p.quit()
                quit(0)
            elif e.type == p.KEYDOWN:
                if e.key == p.K_q:
                    client.send("Q was pressed.")
        screen.fill(p.Color("white"))
        clock.tick(fps)
        p.display.update()


client = pmp.MultiplayerClient(tick_func=loop)
