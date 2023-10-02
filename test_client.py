import pymultiplayer as pmp
import pygame as p
from json import loads, dumps

player = None
other_players = {}


def msg_received(raw_msg):
    print("Received message")
    parsed_msg = loads(raw_msg)
    if parsed_msg["type"] == "sync":
        global other_players
        other_players = dict(parsed_msg["data"])

    elif parsed_msg["type"] == "greeting":
        global player
        player = parsed_msg["data"]
        print(player)


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
                if e.key == p.K_DOWN:
                    player.y += 5
                
                elif e.key == p.K_UP:
                    player.y -= 5
                
                elif e.key == p.K_LEFT:
                    player.x -= 5
                
                elif e.key == p.K_DOWN:
                    player.x += 5

                client.send(dumps({"data": [player.x, player.y]}))

        screen.fill(p.Color("white"))
        for player in other_players.values():
            p.draw.rect(screen, p.Color(player["colour"]), p.Rect(player["x"], player["y"], player["width"], player["height"]))
        clock.tick(fps)
        p.display.update()


client = pmp.MultiplayerClient(tick_func=loop)
client.set_msg_received_func(msg_received)
print("Connecting...")
client.connect()
print("Connected!")
