import gradio as gr
from bot_backend import BotBackend
import time
from flask import Flask, request, jsonify
import threading
import asyncio
from functional import add_code_execution_result_to_bot_history
import json

# Assuming BotBackend and necessary imports are defined elsewhere
bot_backend = BotBackend()
history = []

#add_code_execution_result_to_bot_history("content_to_display", "history", "unique_id")

def execute_python_code(message):
    """
    Handles Python code execution and forms the response for the chatbot.
    """
    print("running")
    try:
        # Here you would send the message to the backend, e.g., using a function to execute code
        response = bot_backend.jupyter_kernel.execute_code(message)
        output = response  # Assuming the backend returns a string output
    except Exception as e:
        output = f"Error: {str(e)}"
    return response[1]

# Create a Gradio app with Chatbot
def run_gradio():
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)


    with gr.Blocks(show_api=True) as app:
        chatbot = gr.Chatbot(placeholder="Type Python code here...")
        
        chatbot.style(height=500)  # Optional, styles the chatbot window
        msg = gr.Textbox(visible=False)
        #add load button
        load = gr.Button("Load")

        app.queue()

        def respond(message, chat_history):
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
        msg.submit(respond, [msg, chatbot], [msg, chatbot], api_name="chatbot")
        load.click(refresh_response, [msg, chatbot], [msg, chatbot, load], api_name="chatbot", every =1)

    app.launch()


# Launch the app
if __name__ == "__main__":

    run_gradio()
    

