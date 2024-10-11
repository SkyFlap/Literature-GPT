import gradio as gr
from pathlib import Path

# current_file_path = Path(__file__).resolve()
# relative_path = "./"
# absolute_path = (current_file_path.parent / ".." / ".." / "gradio").resolve()


def get_file_content(file):
    print(file)
    print(type(file))
    return (file[0],)


with gr.Blocks() as demo:
    gr.Markdown('### `FileExplorer` to `FileExplorer` -- `file_count="multiple"`')
    submit_btn = gr.Button("Select")
    with gr.Row():
        file = gr.FileExplorer(
            height=500,
            glob="*",
            root_dir="./src/output",
            interactive=True,
            show_label=True,
            label="文献资源管理器",
        )
        code = gr.Code(lines=30, scale=2, language="python")
    submit_btn.click(get_file_content, file, code)


if __name__ == "__main__":
    demo.launch()
