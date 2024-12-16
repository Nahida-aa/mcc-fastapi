要检查一个用户的在线状态，通常有几种方法：

1. **基于 WebSocket 的实时通信**：通过 WebSocket 连接来实时跟踪用户的在线状态。当用户连接到 WebSocket 时，标记为在线；当用户断开连接时，标记为离线。

2. **基于心跳机制**：客户端定期发送心跳请求到服务器，服务器记录最后一次心跳时间。如果超过一定时间没有收到心跳请求，则认为用户离线。

3. **基于登录/登出事件**：在用户登录时标记为在线，在用户登出时标记为离线。

以下是一个基于 WebSocket 的示例实现：

### 后端实现

假设你使用的是 FastAPI 和 WebSocket，以下是一个示例实现：

1. **安装依赖**

确保你已经安装了 

fastapi

 和 `uvicorn`：

```bash
pip install fastapi uvicorn
```

2. **创建 WebSocket 端点**

在 `main.py` 中添加 WebSocket 端点：

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"User {user_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"User {user_id} left the chat")
```

3. **运行服务器**

运行 FastAPI 服务器：

```bash
uvicorn main:app --reload
```

### 前端实现

在前端使用 WebSocket 连接到服务器：

```tsx
import { useEffect, useState } from 'react'

export default function Chat({ userId }) {
  const [messages, setMessages] = useState<string[]>([])
  const [input, setInput] = useState('')
  const [socket, setSocket] = useState<WebSocket | null>(null)

  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/${userId}`)
    ws.onmessage = (event) => {
      setMessages((prevMessages) => [...prevMessages, event.data])
    }
    setSocket(ws)

    return () => {
      ws.close()
    }
  }, [userId])

  const sendMessage = () => {
    if (socket) {
      socket.send(input)
      setInput('')
    }
  }

  return (
    <div>
      <div>
        {messages.map((message, index) => (
          <div key={index}>{message}</div>
        ))}
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  )
}
```

### 检查用户在线状态

你可以在 `ConnectionManager` 中维护一个用户在线状态的字典：

```python
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.user_status: Dict[int, bool] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.user_status[user_id] = True

    def disconnect(self, websocket: WebSocket, user_id: int):
        self.active_connections.remove(websocket)
        self.user_status[user_id] = False

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    def is_user_online(self, user_id: int) -> bool:
        return self.user_status.get(user_id, False)

manager = ConnectionManager()

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"User {user_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
        await manager.broadcast(f"User {user_id} left the chat")
```

这样，你就可以通过 `manager.is_user_online(user_id)` 方法来检查用户是否在线。
