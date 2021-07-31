import asyncio  # 웹 소켓 모듈을 선언한다.
import websockets  # 클라이언트 접속이 되면 호출된다.


async def accept(websocket, path):
    while True:
        data = await websocket.recv()
        print("receive : " + data)
        await websocket.send("ws_srv send data = " + data)


start_server = websockets.serve(accept, "0.0.0.0", 4000)

# 비동기로 서버를 대기한다.
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()