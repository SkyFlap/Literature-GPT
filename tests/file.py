import gradio as gr
from pathlib import Path

current_file_path = Path(__file__).resolve()
# relative_path = "./"
absolute_path = (current_file_path.parent / ".." / ".." / "gradio").resolve()


def get_file_content(file):
    return (file,)


def greet(relative_path):
    print(relative_path)
    return relative_path


with gr.Blocks() as demo:
    file_upload = gr.Files(file_count="multiple", file_types=[".pdf"])
    model_apikey = gr.Textbox(scale=3)
    file_upload.upload(fn=greet, inputs=file_upload, outputs=model_apikey)


if __name__ == "__main__":
    demo.launch()
