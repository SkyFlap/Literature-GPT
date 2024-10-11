# Copyright 2024 the Literature-GPT team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import TYPE_CHECKING, Dict


from ...extras.packages import is_gradio_available
from ..common import save_config

if is_gradio_available():
    import gradio as gr

if TYPE_CHECKING:
    from gradio.components import Component
    from ..engine import Engine


def create_preprocess_tab(engine: "Engine") -> Dict[str, "Component"]:
    input_elems = engine.manager.get_base_elems()
    elem_dict = dict()
    with gr.Row():
        with gr.Column():
            file_upload = gr.Files(file_count="multiple", file_types=[".pdf"])
            file_upload_check = gr.Textbox()
        with gr.Column():
            embedding_model = gr.Dropdown(value="智谱AI", choices=["智谱AI"])
            title_input = gr.Textbox(placeholder="请输入论文标题")
            journal_input = gr.Textbox(placeholder="请输入期刊名称（或填入工作论文）")
    preprocess_button = gr.Button()
    preprocess_check = gr.Textbox(show_label=False)
    elem_dict.update(
        dict(
            file_upload=file_upload,
            file_upload_check=file_upload_check,
            embedding_model=embedding_model,
            preprocess_button=preprocess_button,
            preprocess_check=preprocess_check,
            title_input=title_input,
            journal_input=journal_input,
        )
    )
    input_elems.update(
        {file_upload, embedding_model, preprocess_button, title_input, journal_input}
    )
    file_upload.upload(
        fn=engine.runner.check_file,
        inputs=input_elems,
        outputs=file_upload_check,
    )
    preprocess_button.click(
        fn=engine.runner.run_preprocess,
        inputs=input_elems,
        outputs=preprocess_check,
    )
    return elem_dict
