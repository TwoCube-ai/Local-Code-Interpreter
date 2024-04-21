import gradio as gr
from bot_backend import BotBackend
import time
from flask import Flask, request, jsonify
import threading
import asyncio
from functional import add_code_execution_result_to_bot_history
import json

bot_backend = BotBackend()
history = []

def execute_python_code(message):
    """
    Handles Python code execution and forms the response for the chatbot.
    """
    print("running")
    try:
        response = bot_backend.jupyter_kernel.execute_code(message)
        output = response 
    except Exception as e:
        output = f"Error: {str(e)}"
    return response[1]

# Create a Gradio app with Chatbot
def run_gradio():
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)


    with gr.Blocks(show_api=True, css="footer {visibility: hidden}") as app:
        chatbot = gr.Chatbot(placeholder="Type Python code here...", show_label=False)
        
        chatbot.style(height=500) 
        msg = gr.Textbox(visible=False)
        load = gr.Button("Load")

        app.queue()

        def respond(message):
            global history
            response = execute_python_code(message)
            add_code_execution_result_to_bot_history(response, history, "123")
            print(history)
            #save chat history to json
            json.dump(history, open("chat_history.json", "w"))
            # chat_history.append((message, response))
            print(chatbot.__dict__) 
            return message, history
        
        def refresh_response(refresh, chat_history):
            global history
            load.update(visible=False)
            return "", history, gr.Button.update(visible=False)
        

        #call messages event handler
        msg.submit(respond, [msg], [msg, chatbot], api_name="chatbot")
        load.click(refresh_response, [msg, chatbot], [msg, chatbot, load], api_name="chatbot", every =1)

    app.launch()


# Launch the app
if __name__ == "__main__":

    run_gradio()
    

