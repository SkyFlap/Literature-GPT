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

import os

from ..extras.packages import is_gradio_available
from .css import CSS
from .engine import Engine
from .components import (
    create_chat_tab,
    create_top,
    create_literature_tab,
    create_preprocess_tab,
)
from .common import save_config

if is_gradio_available():
    import gradio as gr


def create_ui(demo_mode: bool = False) -> gr.Blocks:
    engine = Engine(demo_mode=demo_mode, pure_chat=False)
    with gr.Blocks(title="Literature GPT", css=CSS) as demo:
        if demo_mode:
            gr.HTML(
                "<h1><center>Literature GPT: A One-stop Web UI for Getting Started with Literature GPT</center></h1>"
            )
            gr.HTML(
                '<h3><center>Visit <a href="https://github.com/SkyFlap/Literature-GPT" target="_blank">'
                "Literature GPT</a> for details.</center></h3>"
            )
            gr.DuplicateButton(
                value="Duplicate Space for private use", elem_classes="duplicate-button"
            )
        engine.manager.add_elems("top", create_top())
        lang: "gr.Dropdown" = engine.manager.get_elem_by_id("top.lang")

        with gr.Tab("Pre-Process"):
            engine.manager.add_elems("preprocess", create_preprocess_tab(engine))

        with gr.Tab("Literature & Chat"):
            engine.manager.add_elems("literature", create_literature_tab(engine))
        with gr.Tab("Chat"):
            engine.manager.add_elems("chat", create_chat_tab(engine))
        demo.load(
            engine.resume,
            outputs=engine.manager.get_elem_list(),
            concurrency_limit=None,
        )
        lang.change(
            engine.change_lang, [lang], engine.manager.get_elem_list(), queue=False
        )
        lang.input(save_config, inputs=[lang], queue=False)
    return demo
