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
from typing import TYPE_CHECKING, Dict, Tuple, Any

if TYPE_CHECKING:
    from gradio.components import Component

    from ..engine import Engine
from ...extras.packages import is_gradio_available
from ..utils import check_json_schema

if is_gradio_available():
    import gradio as gr


def create_survey_box(
    input_elems: Dict["Component", Any], engine: "Engine", visible: bool = False
) -> Tuple["Component", "Component", Dict[str, "Component"]]:
    with gr.Column(visible=visible) as survey_box:
        survey_bot = gr.Textbox(show_copy_button=True)
        generate_survey_button = gr.Button("generate survey")
        generate_abstract_button = gr.Button("generate abstract")
        abstract_downloadbutton = gr.DownloadButton(visible=False)
        survey_downloadbutton = gr.DownloadButton(visible=False)
    generate_survey_button.click(
        engine.runner.generate_survey,
        input_elems,
        [survey_bot, abstract_downloadbutton, survey_downloadbutton],
    )
    generate_abstract_button.click(
        engine.runner.generate_abstract,
        input_elems,
        [survey_bot, abstract_downloadbutton],
    )
    return dict(
        survey_box=survey_box,
        survey_bot=survey_bot,
        generate_survey_button=generate_survey_button,
        generate_abstract_button=generate_abstract_button,
        abstract_downloadbutton=abstract_downloadbutton,
        survey_downloadbutton=survey_downloadbutton,
    )
