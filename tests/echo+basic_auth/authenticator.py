import websockets
import asyncio


async def proxy(websocket):
    print("Connected")
    await websocket.send("login")
    name = await websocket.recv()
    password = await websocket.recv()
    with open("users.txt", "r") as f:
        users = [user for user in f.read().split("\n")]

    if f"{name} {password}" in users:
        await websocket.send("success")

    else:
        await websocket.send("failure")



async def main():
    async with websockets.serve(proxy, "localhost", 3000):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
