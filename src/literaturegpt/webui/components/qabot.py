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

import json
from typing import TYPE_CHECKING, Dict, Tuple, Any

if TYPE_CHECKING:
    from gradio.components import Component

    from ..engine import Engine
from ...extras.packages import is_gradio_available
from ..utils import check_json_schema
from ...prompt.qabot import PROMPT
from ...retrievers.hybrid_search import hybrid_search

if is_gradio_available():
    import gradio as gr


def parse_text(text):
    lines = text.split("\n")
    lines = [line for line in lines if line != ""]
    count = 0
    for i, line in enumerate(lines):
        if "```" in line:
            count += 1
            items = line.split("`")
            if count % 2 == 1:
                lines[i] = f'<pre><code class="language-{items[-1]}">'
            else:
                lines[i] = f"<br></code></pre>"
        else:
            if i > 0:
                if count % 2 == 1:
                    line = line.replace("`", "\`")
                    line = line.replace("<", "&lt;")
                    line = line.replace(">", "&gt;")
                    line = line.replace(" ", "&nbsp;")
                    line = line.replace("*", "&ast;")
                    line = line.replace("_", "&lowbar;")
                    line = line.replace("-", "&#45;")
                    line = line.replace(".", "&#46;")
                    line = line.replace("!", "&#33;")
                    line = line.replace("(", "&#40;")
                    line = line.replace(")", "&#41;")
                    line = line.replace("$", "&#36;")
                lines[i] = "<br>" + line
    text = "".join(lines)
    return text


def create_qa_box(
    input_elems: Dict["Component", Any], engine: "Engine", visible: bool = False
) -> Tuple["Component", "Component", Dict[str, "Component"]]:
    with gr.Column(visible=visible) as qa_box:
        qabot = gr.Chatbot(show_copy_button=True)
        with gr.Row():
            with gr.Column(scale=3):
                with gr.Column(scale=12):
                    user_qainput = gr.Textbox(
                        show_label=False,
                        placeholder="Input...",
                        lines=10,
                        container=False,
                    )
                with gr.Column(min_width=32, scale=1):
                    qa_submitBtn = gr.Button("Submit")
            with gr.Column(scale=1):
                qa_emptyBtn = gr.Button("Clear History")
                max_length = gr.Slider(
                    0,
                    8192,
                    value=1024,
                    step=1.0,
                    label="Maximum length",
                    interactive=True,
                )
                top_p = gr.Slider(
                    0.01, 1, value=0.95, step=0.01, label="Top P", interactive=True
                )
                temperature = gr.Slider(
                    0.01, 1, value=0.7, step=0.01, label="Temperature", interactive=True
                )
    input_elems.update(
        {
            top_p,
            max_length,
            temperature,
            qabot,
            user_qainput,
        }
    )

    def user(query, history):
        print(history + [[parse_text(query), ""]])
        return "", history + [[parse_text(query), ""]]

    qa_submitBtn.click(
        user, [user_qainput, qabot], [user_qainput, qabot], queue=False
    ).then(
        fn=engine.chatter.stream,
        inputs=input_elems,
        outputs=qabot,
    )
    qa_emptyBtn.click(lambda: (None), None, [qabot], queue=False)
    return dict(
        qa_box=qa_box,
        qabot=qabot,
        user_qainput=user_qainput,
        qa_submitBtn=qa_submitBtn,
        qa_emptyBtn=qa_emptyBtn,
        max_length=max_length,
        top_p=top_p,
        temperature=temperature,
    )
