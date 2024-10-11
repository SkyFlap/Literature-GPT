import gradio as gr
import os

latex_delimiters_set = [
    {"left": "$$", "right": "$$", "display": True},
    {"left": "$", "right": "$", "display": False},
    {"left": "\\(", "right": "\\)", "display": False},
    {"left": "\\[", "right": "\\]", "display": True},
    {"left": "\\begin{equation}", "right": "\\end{equation}", "display": True},
    {"left": "\\begin{align}", "right": "\\end{align}", "display": True},
    {"left": "\\begin{alignat}", "right": "\\end{alignat}", "display": True},
    {"left": "\\begin{gather}", "right": "\\end{gather}", "display": True},
    {"left": "\\begin{CD}", "right": "\\end{CD}", "display": True},
]


def get_content(filename):
    path = os.path.join("./tests", filename)
    if os.path.exists(path):
        with open(path, encoding="utf8") as file:
            return file.read()
    return ""


with gr.Blocks() as demo:
    with gr.Column():
        chatbot = gr.Chatbot(
            label="Chuanhu Chat",
            elem_id="chuanhu-chatbot",
            latex_delimiters=latex_delimiters_set,
            sanitize_html=False,
            # height=700,
            show_label=False,
            avatar_images=["./tests/user.png", "./tests/openai-black.png"],
            show_share_button=False,
            placeholder=get_content("chatbot_placeholder.md"),
        )
        with gr.Row():
            user_input = gr.Textbox(
                show_label=False, placeholder="在这里输入", max_lines=5, min_width=420,scale=12
            )
            submitBtn = gr.Button(value="提交", variant="primary",scale=1)
demo.title = "Chat 🚀"
if __name__ == "__main__":
    os.environ["GRADIO_SHARE"] = "true"
    gradio_share = os.environ.get("GRADIO_SHARE", "0").lower() in ["true", "1"]
    server_name = os.environ.get("GRADIO_SERVER_NAME", "0.0.0.0")
    demo.queue().launch(
        share=gradio_share, server_name=server_name, inbrowser=True
    )
