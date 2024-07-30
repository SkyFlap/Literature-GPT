import gradio as gr
from pathlib import Path

current_file_path = Path(__file__).resolve()
relative_path = "./"
absolute_path = (current_file_path.parent / ".." / ".." / "gradio").resolve()


def get_file_content(file):
    return file


with gr.Blocks() as demo:
    gr.Markdown('### `FileExplorer` to `FileExplorer` -- `file_count="multiple"`')
    submit_btn = gr.Button("Select")
    with gr.Row():
        file = gr.FileExplorer(
            glob="*",
            root_dir="./src/literature_db",
            interactive=True,
            show_label=True,
            label="文献资源管理器",
        )
        txt = gr.Textbox()
    submit_btn.click(get_file_content, file, txt)


if __name__ == "__main__":
    demo.launch()
