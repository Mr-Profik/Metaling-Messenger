
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Dict
import uvicorn

app = FastAPI(title="Metaling Ultimate API")

# CORS для связи с Android/Web
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# --- БАЗА ДАННЫХ (Эмуляция) ---
users: Dict[str, dict] = {}
messages: List[dict] = []
groups: List[dict] = []
channels: List[dict] = []
market_items: List[dict] = [
    {"id": 1, "name": "Premium Badge", "price": "5.0 LIME", "type": "digital"},
    {"id": 2, "name": "AI Pro Subscription", "price": "10.0 LIME", "type": "service"}
]

# --- МОДЕЛИ ---
class UserProfile(BaseModel):
    username: str
    display_name: str
    bio: Optional[str] = ""
    avatar_url: Optional[str] = ""
    status: Optional[str] = "Online"

class ChatMessage(BaseModel):
    sender: str
    text: str
    source: str = "Metaling" # TG, WA, Discord, Metaling
    chat_type: str = "private" # private, group, channel

# --- АККАУНТ И ПРОФИЛЬ ---
@app.post("/auth/register")
def register(u: UserProfile):
    if u.username in users: raise HTTPException(400, "Username taken")
    users[u.username] = u.dict()
    return {"status": "created", "user": users[u.username]}

@app.get("/profile/{username}")
def get_profile(username: str):
    if username not in users: raise HTTPException(404, "Not found")
    return users[username]

# --- ЧАТЫ И СООБЩЕНИЯ ---
@app.post("/chat/send")
def send_msg(m: ChatMessage):
    new_msg = m.dict()
    new_msg["id"] = len(messages) + 1
    new_msg["time"] = datetime.now().strftime("%H:%M")
    messages.append(new_msg)
    return new_msg

@app.get("/chat/history")
def get_history(limit: int = 20):
    return messages[-limit:]

# --- ГЛОБАЛЬНЫЙ ПОИСК ---
@app.get("/search")
def search(q: str):
    results = [m for m in messages if q.lower() in m["text"].lower()]
    return {"query": q, "results": results}

# --- ГРУППЫ И КАНАЛЫ ---
@app.post("/groups/create")
def create_group(name: str, owner: str):
    group = {"id": len(groups)+1, "name": name, "owner": owner, "members": [owner]}
    groups.append(group)
    return group

# --- MARKETPLACE ---
@app.get("/market/items")
def get_market():
    return market_items

# --- METALING AI ---
@app.get("/ai/summarize")
def ai_summarize():
    if not messages: return {"summary": "Сообщений пока нет."}
    # Заглушка для AI
    return {"summary": f"Краткая сводка последних {len(messages)} сообщений: Обсуждение проекта Metaling."}

@app.get("/")
def status():
    return {"engine": "Metaling", "uptime": "100%", "services": ["Chat", "AI", "Market", "Cloud"]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
