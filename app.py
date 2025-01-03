
from openai import OpenAI
import gradio as gr
from anthropic import Anthropic


import os
from dotenv import load_dotenv
load_dotenv()
openai_api_key = os.environ.get('OPENAI_API_KEY','')
anthropic_api_key = os.environ.get('ANTHROPIC_API_KEY','')
google_api_key = os.environ.get('GOOGLE_API_KEY','')


def openai_api_stream_chat(openai_instance,model,history):
    stream = openai_instance.chat.completions.create(model=model, messages=history, stream=True)
    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        yield response



openai = OpenAI(api_key=openai_api_key)
def openai_stream_chat(model,history):
    return openai_api_stream_chat(openai,model,history)


gemini_client = OpenAI(api_key=google_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
def gemini_stream_chat(model,history):
    return openai_api_stream_chat(gemini_client,model,history)


anthropic = Anthropic(api_key=anthropic_api_key)
def claude_stream_chat(model, history,system_message):

    # Create streaming response
    stream = anthropic.messages.create(
        model=model,
        messages=history,
        stream=True,
        max_tokens=4096,
        system = system_message
    )

    response = ""
    for chunk in stream:
        if chunk.type == "content_block_delta":
            response += chunk.delta.text or ''
            yield response

import re
def is_not_blank(string):
    return bool(re.search(r'\S', string))

model_options = []
if anthropic_api_key and is_not_blank(anthropic_api_key):
    model_options.append("claude-3-5-sonnet-20240620")
    # add more Anthropic models if required
if openai_api_key and is_not_blank(openai_api_key):
    model_options.append("gpt-4o")
    model_options.append("o1-preview")
    model_options.append("o1-mini")
    model_options.append("gpt-3.5-turbo")
    # add more OpenAI models if required
if google_api_key and is_not_blank(google_api_key):
    model_options.append("gemini-1.5-flash")
    # add more Gemini models if required

if len(model_options) == 0:
  raise ValueError('Need at least one model to run')
css = """
.custom-row {
    display: flex;
    align-items: center;
}
footer {display: none !important}
.gradio-container {min-height: 0px !important}
"""
def call_llm(history, selected_model: str,system_message):
    print(system_message)
    cleaned_history = []
    if system_message and is_not_blank(system_message) and (not 'claude' in selected_model) and (not 'o1' in selected_model):
        cleaned_history.append({"role": 'system', "content": system_message})
    if system_message and is_not_blank(system_message) and ('o1' in selected_model):
        cleaned_history.append({"role": 'user', "content": system_message})
    for msg in history:
        cleaned_history.append({"role": msg["role"], "content": msg["content"]})
    if 'gpt' in selected_model or 'o1' in selected_model:
        return openai_stream_chat(selected_model, history=cleaned_history)
    elif 'claude' in selected_model:
        return claude_stream_chat(selected_model, history=cleaned_history,system_message=system_message)
    elif 'gemini' in selected_model:
        return gemini_stream_chat(selected_model, history=cleaned_history)

with gr.Blocks(css=css,title= 'LLM chatbots') as ui:
    selected_model = gr.State(value=model_options[0])  # Use gr.State to store the current model

    dropdown = gr.Dropdown(
        label="Choose a model",
        choices=model_options,
        interactive=True,
        value=model_options[0]
    )
    
    system_message = gr.Textbox(label="System message:")

    chatbot = gr.Chatbot(height=500, type="messages")
    entry = gr.Textbox(label="Chat with our AI Assistant:")
    clear = gr.Button("Clear")

    def update_model(new_model):
        return new_model

    def do_entry(message, history, current_model,system_message_text):
        history += [{"role": "user", "content": message}]
        yield "", history
        for chunk in call_llm(history, current_model,system_message_text):
            yield '', [*history, {"role": "assistant", "content": chunk}]

    # Update the model state when dropdown changes
    dropdown.change(
        update_model,
        inputs=[dropdown],
        outputs=[selected_model]
    )

    # Pass the current model state to do_entry
    entry.submit(
        do_entry,
        inputs=[entry, chatbot, selected_model,system_message],
        outputs=[entry, chatbot]
    )

    clear.click(lambda: None, inputs=None, outputs=chatbot, queue=False)

ui.launch(inbrowser=True,share=True, server_name="0.0.0.0")

