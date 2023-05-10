import pymultiplayer as pmp
from time import sleep

pmp.connect(2011)
socket = pmp.get_socket()
send = input("Send data? (Y/N): ")
if send.upper() == "Y":
    pmp.send(socket, "print('Hello world!')")
pmp.update(socket)
