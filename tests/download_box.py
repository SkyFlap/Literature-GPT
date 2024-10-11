from pathlib import Path
import gradio as gr


def upload_file(filepath_list):
    name = Path(filepath_list[0]).name
    return [
        gr.UploadButton(visible=False),
        gr.Files(
            label=f"Download {name}",
            file_count="multiple",
            value=filepath_list,
            visible=True,
        ),
    ]


def download_file():
    return [gr.UploadButton(visible=True), gr.Files(visible=False)]


with gr.Blocks() as demo:
    gr.Markdown(
        "First upload a file and and then you'll be able download it (but only once!)"
    )
    with gr.Row():
        u = gr.UploadButton("Upload a file", file_count="multiple")
        d = gr.Files(visible=False)

    u.upload(upload_file, u, [u, d])


if __name__ == "__main__":
    demo.launch()
