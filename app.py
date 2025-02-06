import gradio as gr
import outlook_agent, auth
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

CUSTOM_PATH = "/gradio"

app = FastAPI()

def get_token(request: Request):
    token = auth.get_access_token(["User.Read", "Tasks.ReadWrite"])
    return token

def outlook_agent_chat(message, history):
    new_message = outlook_agent.chat(message)
    return new_message

@app.get("/")
def read_main():
    return RedirectResponse(url=CUSTOM_PATH)

io = gr.ChatInterface(
    fn=outlook_agent_chat,
    type="messages",
)

app = gr.mount_gradio_app(app, io, path=CUSTOM_PATH, auth_dependency=get_token)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)