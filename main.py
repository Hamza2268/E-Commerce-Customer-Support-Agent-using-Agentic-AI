import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import run_agent_loop, SESSION_STORE
import uvicorn

app = FastAPI(title="E-Commerce Agent API")

class ChatRequest(BaseModel):
    message: str
    session_id: str = None

class ChatResponse(BaseModel):
    reply: str
    session_id: str

################################# conversational interactions #################################
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    session_id = request.session_id or str(uuid.uuid4())
    
    reply = run_agent_loop(session_id, request.message)
    
    return ChatResponse(reply=reply, session_id=session_id)

################################# Debugging endpoint to retrieve message history #################################
@app.get("/history/{session_id}")
async def get_history(session_id: str):
    if session_id not in SESSION_STORE:
        raise HTTPException(status_code=404, detail="Session not found.")
    return {"session_id": session_id, "history": SESSION_STORE[session_id]}

################################ Endpoint to clear a conversational session #################################
@app.delete("/reset/{session_id}")
async def reset_session(session_id: str):
    if session_id in SESSION_STORE:
        del SESSION_STORE[session_id]
        return {"status": "success", "message": f"Session {session_id} cleared."}
    raise HTTPException(status_code=404, detail="Session not found.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)