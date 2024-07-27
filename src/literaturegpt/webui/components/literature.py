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


def create_literature_tab(engine: "Engine") -> Dict[str, "Component"]:
    input_elems = engine.manager.get_base_elems()
    elem_dict = dict()
    model_apikey = gr.Textbox(scale=3)
    with gr.Row():
        file_3 = gr.FileExplorer(
            scale=1,
            glob="*.pdf",
            file_count="multiple",
            root_dir=relative_path,
            ignore_glob="**/__init__.py",
            elem_id="file",
        )

        code = gr.Code(lines=30, scale=2, language="python")
    return elem_dict
