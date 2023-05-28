import pymultiplayer as pmp
import pygame as p
from rel import dispatch


def msg_received(msg):
    print(f"Server sent message: {msg}")


def init():
    p.init()
    p.display.set_mode((100, 100))
    p.display.update()
    p.display.set_caption("Test Client")


def loop(*args):
    client = args[0][0]
    while True:
        for e in p.event.get():
            if e.type == p.QUIT:
                client.disconnect()
                quit()
            elif e.type == p.KEYDOWN:
                if e.key == p.K_q:
                    print(client.send)
                    client.send("Hello from client!")
                    print("Sent message to server.")
        p.display.update()
        return True


init()

# Create a client object
client = pmp.MultiplayerClient(tick_func=loop)

client.set_msg_received_func(msg_received)
