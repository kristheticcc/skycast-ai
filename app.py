# Imports
import gradio as gr
from chat import chat, put_message_in_chatbox

# build_ui: Generates the gradio UI for the assistant
def build_ui():
    with gr.Blocks() as ui:
        gr.Markdown("# Skycast AI 🌤️")
        with gr.Row():
            chatbot = gr.Chatbot(height = 500)
            image_output = gr.Image(height = 500, interactive = False)
        with gr.Row():
            audio_output = gr.Audio(interactive = False, autoplay = True)

        with gr.Row():
            message = gr.Textbox(label = "Chat with Skycast: ")

        message.submit(
                        put_message_in_chatbox,
                        inputs = [message, chatbot],
                        outputs = [message, chatbot]
                ).then(
                        chat,
                        inputs = [chatbot],
                        outputs = [chatbot, audio_output, image_output]
                    )
    return ui


ui = build_ui()
ui.launch()



