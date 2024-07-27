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


from ...extras.constants import SUPPORTED_MODELS
from ...extras.packages import is_gradio_available
from ..common import save_config

if is_gradio_available():
    import gradio as gr


from gradio.components import Component


def create_top() -> Dict[str, "Component"]:
    available_models = list(SUPPORTED_MODELS) + ["Custom"]

    with gr.Row():
        lang = gr.Dropdown(choices=["zh"], scale=1)
        model_name = gr.Dropdown(choices=available_models, scale=3)
        model_apikey = gr.Textbox(scale=3)
        model_name.input(save_config, inputs=[lang, model_name], queue=False)
        model_apikey.input(
            save_config, inputs=[lang, model_name, model_apikey], queue=False
        )
    return dict(lang=lang, model_name=model_name, model_apikey=model_apikey)
