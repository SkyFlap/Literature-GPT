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


from gradio.components import Component
from ..engine import Engine


def create_preprocess_tab(engine: "Engine") -> Dict[str, "Component"]:
    input_elems = engine.manager.get_base_elems()
    lang: "gr.Dropdown" = engine.manager.get_elem_by_id("top.lang")
    elem_dict = dict()
    file_upload = gr.Files(file_count="multiple", file_types=[".pdf"])
    file_upload_check = gr.Textbox(scale=3)
    preprocess_button = gr.Button()
    preprocess_check = gr.Textbox(scale=3)
    elem_dict.update(
        dict(
            file_upload=file_upload,
            file_upload_check=file_upload_check,
            preprocess_button=preprocess_button,
            preprocess_check=preprocess_check,
        )
    )
    file_upload.upload(
        fn=engine.runner.check_file,
        inputs=[lang, file_upload],
        outputs=file_upload_check,
    )
    preprocess_button.click(
        fn=engine.runner.run_preprocess,
        inputs=[lang, file_upload],
        outputs=preprocess_check,
    )
    return elem_dict
