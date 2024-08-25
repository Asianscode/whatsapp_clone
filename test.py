import websocket

try:
    ws = websocket.WebSocket()
    ws.connect("ws://localhost:8000/ws/signaling/")
    print("Connected to the server")
    ws.close()
except websocket.WebSocketConnectionClosedException as e:
    print("WebSocket connection was closed:", e)
except Exception as e:
    print("An error occurred:", e)
