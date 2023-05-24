import pymultiplayer as pmp
import pygame as p


def msg_received(msg):
    print(f"Server sent message: {msg}")


def loop():
    print("in loop")
    p.init()
    print("before display")
    p.display.set_mode((100, 100))
    print("here")
    p.display.update()
    p.display.set_caption("Test Client")
    while True:
        for e in p.event.get():
            if e.type == p.QUIT:
                client.disconnect()
                quit()
            elif e.type == p.KEYDOWN:
                if e.key == p.K_q:
                    client.send("Hello from client!")
        p.display.update()
    return True


# Create a client object
client = pmp.MultiplayerClient(tick_func=loop)

client.set_msg_received_func(msg_received)
