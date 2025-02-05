import gradio as gr
import outlook_agent
import random

def outlook_agent_chat(message, history):
    new_message = outlook_agent.chat(message)
    return new_message

def random_response(message, history):
    if len([h for h in history if h['role'] == "assistant"]) % 2 == 0:
        return f"Yes, I do think that: {message}"
    else:
        return f"No, I don't think that: {message}"

def greet(name, intensity):
    return "Hello, " + name + "!" * int(intensity)

ui = gr.ChatInterface(
    fn=outlook_agent_chat,
    type="messages",
)

ui.launch()