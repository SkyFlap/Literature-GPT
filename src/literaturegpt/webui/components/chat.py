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
from .chatbot import create_chat_box
from .surveybot import create_survey_box
from ..common import save_config
from ...extras.packages import is_gradio_available


if is_gradio_available():
    import gradio as gr


def create_chat_tab(engine: "Engine") -> Dict[str, "Component"]:
    input_elems = engine.manager.get_base_elems()
    elem_dict = dict()
    load_chat_button = gr.Button()
    chatbot, messages, chat_elems = create_chat_box(engine, visible=False)
    
    
    elem_dict.update(
        dict(
            load_chat_button=load_chat_button,
        )
    )
    input_elems.update({load_chat_button})
    elem_dict.update(chat_elems)
    elem_dict.update(dict(chatbot=chatbot))
    load_chat_button.click(
        lambda: gr.Column(visible=True),
        outputs=[chat_elems["chat_box"]],
    )
    return elem_dict
