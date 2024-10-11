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


from typing import TYPE_CHECKING, Dict, Tuple

if TYPE_CHECKING:
    from gradio.components import Component

    from ..engine import Engine
from .qabot import create_qa_box
from .surveybot import create_survey_box
from ..common import save_config
from ...extras.packages import is_gradio_available


if is_gradio_available():
    import gradio as gr


def create_literature_tab(engine: "Engine") -> Dict[str, "Component"]:
    input_elems = engine.manager.get_base_elems()
    elem_dict = dict()
    literature_select_button = gr.Button()
    with gr.Row():
        literature_explorer = gr.FileExplorer()
        literature_check = gr.Textbox()
    with gr.Accordion(open=True) as mode_tab:
        with gr.Row():
            qa_mode_button = gr.Button()
            survey_mode_button = gr.Button()
    elem_dict.update(
        dict(
            literature_select_button=literature_select_button,
            literature_explorer=literature_explorer,
            literature_check=literature_check,
            mode_tab=mode_tab,
            qa_mode_button=qa_mode_button,
            survey_mode_button=survey_mode_button,
        )
    )
    input_elems.update({literature_explorer})
    qa_elems = create_qa_box(input_elems, engine, visible=False)
    elem_dict.update(qa_elems)
    survey_elems = create_survey_box(input_elems, engine, visible=False)
    elem_dict.update(survey_elems)
    literature_select_button.click(
        engine.runner.literature_check, input_elems, literature_check
    )
    qa_mode_button.click(
        lambda: gr.Column(visible=True),
        outputs=[qa_elems["qa_box"]],
    )
    survey_mode_button.click(
        lambda: gr.Column(visible=True),
        outputs=[survey_elems["survey_box"]],
    )
    return elem_dict
