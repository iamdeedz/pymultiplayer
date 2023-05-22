import pymultiplayer as pmp


def msg_received(msg):
    print(f"Server sent message: {msg}")


print("before connection")
# Create a client object
client = pmp.MultiplayerClient()

print("after connection")

client.set_msg_received_func(msg_received)

client.send("Hello from client!")
