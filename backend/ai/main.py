import os
import sys
import tempfile
import gradio as gr

# Ensure backend and ai directory are in sys.path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

ai_dir = os.path.dirname(__file__)
if ai_dir not in sys.path:
    sys.path.insert(0, ai_dir)

from speech import Speech
from engine import generate_response


def to_gradio_chatbot_format(history):
    """Converts engine chat history list into Gradio 6 Chatbot messages format."""
    if not history:
        return []
    formatted = []
    for item in history:
        role = item.get("role", "user")
        content = item.get("message") or item.get("content", "")
        formatted.append({"role": role, "content": content})
    return formatted


def process_text_query(user_message, history, tts_enabled):
    """Processes text input message, calls engine, and generates TTS response if enabled."""
    if history is None:
        history = []

    if not user_message or not user_message.strip():
        return "", to_gradio_chatbot_format(history), "", "", None, history

    # Call AI engine
    result = generate_response(user_message, chat_history=history)
    response_text = result.get("response", "")
    intent = result.get("intent", "Unknown")
    context = result.get("context", "")
    updated_history = result.get("chat_history", history)

    # Format history as [{"role": ..., "content": ...}] for Gradio 6 Chatbot display
    formatted_chat = to_gradio_chatbot_format(updated_history)

    # Generate TTS audio file if enabled
    audio_path = None
    if tts_enabled and response_text:
        try:
            audio_path = Speech.speak_to_file(response_text)
        except Exception as err:
            print("Speech TTS Error:", err)
            audio_path = None

    return "", formatted_chat, intent, context, audio_path, updated_history


def process_audio_query(audio_file, history, tts_enabled):
    """Transcribes user voice recording and processes the query."""
    if history is None:
        history = []

    if audio_file is None:
        return to_gradio_chatbot_format(history), "", "", None, history

    # Perform Speech-To-Text transcription
    transcribed_text = Speech.stt(audio_file)
    if not transcribed_text or not transcribed_text.strip():
        return to_gradio_chatbot_format(history), "Voice STT", "No speech detected in audio.", None, history

    # Delegate to process_text_query with transcribed text
    _, formatted_chat, intent, context, audio_path, updated_history = process_text_query(
        transcribed_text, history, tts_enabled
    )

    return formatted_chat, intent, context, audio_path, updated_history


def clear_chat():
    """Clears conversation state and UI elements."""
    return [], "", "", None, []



def create_app():
    """Builds and returns the Gradio Blocks UI."""
    custom_css = """
    .main-title {
        text-align: center;
        margin-bottom: 10px;
    }
    .main-subtitle {
        text-align: center;
        color: red;
        margin-bottom: 20px;
    }
    """

    with gr.Blocks(title="Support AI Assistant") as demo:
        # Chat history state stored per session
        history_state = gr.State(value=[])

        gr.Markdown(
            """
            # 🤖 Support AI Assistant
            ### *Smart E-Commerce Support Powered by LLM & Voice*
            """,
            elem_classes=["main-title"]
        )

        with gr.Row():
            # Main Chat Interaction Column
            with gr.Column(scale=7):
                chatbot = gr.Chatbot(
                    label="💬 Support Chat",
                    height=450
                )

                with gr.Row():
                    text_input = gr.Textbox(
                        placeholder="Type your question here (e.g. 'What products do you have?' or 'Status of ord101')...",
                        label="Your Message",
                        scale=8,
                        lines=1
                    )
                    send_btn = gr.Button("Send 📤", variant="primary", scale=2)

                with gr.Row():
                    audio_input = gr.Audio(
                        sources=["microphone", "upload"],
                        type="filepath",
                        label="🎙️ Voice Input (Record Microphone or Upload Audio)",
                        scale=7
                    )
                    voice_send_btn = gr.Button("Submit Voice 🗣️", variant="secondary", scale=3)

                with gr.Row():
                    clear_btn = gr.Button("🗑️ Clear Chat History", variant="stop")
                    tts_checkbox = gr.Checkbox(label="🔊 Enable Spoken Voice Response (TTS)", value=True)

                audio_output = gr.Audio(
                    label="🔊 Assistant Spoken Response",
                    autoplay=True,
                    interactive=False
                )

            # Insights / Debug Panel Column
            with gr.Column(scale=4):
                gr.Markdown("### 🔍 AI Insights & Context")

                intent_output = gr.Textbox(
                    label="🎯 Detected Intent",
                    interactive=False,
                    placeholder="Intent classification will appear here..."
                )

                context_output = gr.Textbox(
                    label="📚 Database Context Retrieved",
                    interactive=False,
                    lines=12,
                    placeholder="Database information fetched for your query will appear here..."
                )


        # Event listeners for text input
        text_input.submit(
            fn=process_text_query,
            inputs=[text_input, history_state, tts_checkbox],
            outputs=[text_input, chatbot, intent_output, context_output, audio_output, history_state]
        )
        send_btn.click(
            fn=process_text_query,
            inputs=[text_input, history_state, tts_checkbox],
            outputs=[text_input, chatbot, intent_output, context_output, audio_output, history_state]
        )

        # Event listeners for voice input
        voice_send_btn.click(
            fn=process_audio_query,
            inputs=[audio_input, history_state, tts_checkbox],
            outputs=[chatbot, intent_output, context_output, audio_output, history_state]
        )
        audio_input.stop_recording(
            fn=process_audio_query,
            inputs=[audio_input, history_state, tts_checkbox],
            outputs=[chatbot, intent_output, context_output, audio_output, history_state]
        )

        # Clear chat event listener
        clear_btn.click(
            fn=clear_chat,
            inputs=[],
            outputs=[chatbot, intent_output, context_output, audio_output, history_state]
        )

    return demo


if __name__ == "__main__":
    demo = create_app()
    print("Launching Support AI Gradio Interface on http://127.0.0.1:7860 ...")
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False)