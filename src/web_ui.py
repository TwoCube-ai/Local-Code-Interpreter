import gradio as gr
from bot_backend import BotBackend
from functional import add_code_execution_result_to_bot_history
import json
import asyncio

bot_backend = BotBackend()
history = []
files = []

def execute_python_code(message):
    """
    Handles Python code execution and forms the response for the chatbot.
    """
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

    with gr.Blocks(
            theme=gr.themes.Glass(),
            css="footer {visibility: hidden}"
            ) as app:
        
        chatbot = gr.Chatbot(show_label=False, height=500)
        
        msg = gr.Textbox(visible=False)
        load = gr.Button("Load")

        file_upload_button = gr.UploadButton("Upload 📁", file_count='single')

        app.queue()

        def respond(message):
            global history
            response = execute_python_code(message)
            history.append([None, f"```{message}```"])
            add_code_execution_result_to_bot_history(response, history, "unique_id")
            json.dump(history, open("chat_history.json", "w"))
            print(chatbot.__dict__) 
            return message, history
        
        def refresh_response(refresh, chat_history):
            global history
            load.update(visible=False)
            return "", history, gr.Button.update(visible=False)
        
        def upload(file):
            global history
            global files
            print(file)
            files.append(file)
            history.append([None, f"Uploaded: {file.name}"])
            return file, history, files
    
        file_locations = gr.State([])
        msg.submit(respond, [msg], [msg, chatbot])
        load.click(refresh_response, [msg, chatbot], [msg, chatbot, load], every =1)
        file_upload_button.upload(upload, [file_upload_button], [msg, chatbot, file_locations])

        app.launch()
        


# Launch the app
if __name__ == "__main__":
    run_gradio()
    

