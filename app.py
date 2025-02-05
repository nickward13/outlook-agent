import gradio as gr
import outlook_agent
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

CUSTOM_PATH = "/gradio"

app = FastAPI()

@app.get("/")
def read_main():
    return RedirectResponse(url=CUSTOM_PATH)

def outlook_agent_chat(message, history):
    new_message = outlook_agent.chat(message)
    return new_message

io = gr.ChatInterface(
    fn=outlook_agent_chat,
    type="messages"
)

app = gr.mount_gradio_app(app, io, path=CUSTOM_PATH)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)