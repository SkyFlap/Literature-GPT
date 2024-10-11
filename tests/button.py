from pathlib import Path
import gradio as gr


def upload_file(filepath):
    name = Path(filepath).name
    return [
        gr.UploadButton(visible=True),
        gr.DownloadButton(label=f"Download {name}", value=filepath, visible=True),
        filepath,
    ]


def download_file():
    return [gr.UploadButton(visible=True), gr.DownloadButton(visible=False)]


with gr.Blocks() as demo:
    gr.Markdown(
        "First upload a file and and then you'll be able download it (but only once!)"
    )
    u = gr.UploadButton("Upload a file", file_count="single")
    d = gr.DownloadButton("Download the file", visible=False)
    text = gr.Textbox()
    t = gr.DownloadButton(value="./src/cache/user_config.yaml")

    u.upload(upload_file, u, [u, d, text])
    d.click(download_file, None, [u, d])


if __name__ == "__main__":
    demo.launch()
