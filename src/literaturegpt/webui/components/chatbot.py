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
from ...data import Role
from ...extras.packages import is_gradio_available
from ..utils import check_json_schema

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


def predict(
    model_name, api_key, history, prompt, max_length=4096, top_p=0.7, temperature=0.95
):
    messages = []
    print(history)
    if prompt:
        messages.append({"role": "system", "content": prompt})
    for idx, (user_msg, model_msg) in enumerate(history):
        if prompt and idx == 0:
            continue
        if idx == len(history) - 1 and not model_msg:
            messages.append({"role": "user", "content": user_msg})
            break
        if user_msg:
            messages.append({"role": "user", "content": user_msg})
        if model_msg:
            messages.append({"role": "assistant", "content": model_msg})
    from zhipuai import ZhipuAI

    client = ZhipuAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        max_tokens=max_length,
        top_p=top_p,
        temperature=temperature,
        stream=True,
    )
    for chunk in response:
        history[-1][1] += chunk.choices[0].delta.content
        yield history


def create_chat_box(
    engine: "Engine", visible: bool = False
) -> Tuple["Component", "Component", Dict[str, "Component"]]:
    model_name, api_key = engine.manager.get_elem_by_id(
        "top.model_name"
    ), engine.manager.get_elem_by_id("top.model_apikey")
    with gr.Column(visible=visible) as chat_box:
        chatbot = gr.Chatbot(show_copy_button=True)
        messages = gr.State([])
        with gr.Row():
            with gr.Column(scale=3):
                with gr.Column(scale=12):
                    user_input = gr.Textbox(
                        show_label=False,
                        placeholder="Input...",
                        lines=10,
                        container=False,
                    )
                with gr.Column(min_width=32, scale=1):
                    submitBtn = gr.Button("Submit")
            with gr.Column(scale=1):
                prompt_input = gr.Textbox(
                    show_label=False, placeholder="Prompt", lines=10, container=False
                )
                with gr.Row():
                    pBtn = gr.Button("Set Prompt")
            with gr.Column(scale=1):
                emptyBtn = gr.Button("Clear History")
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

    def user(query, history):
        return "", history + [[parse_text(query), ""]]

    def set_prompt(prompt_text):
        return [[parse_text(prompt_text), "成功设置prompt"]]

    pBtn.click(set_prompt, inputs=[prompt_input], outputs=chatbot)

    submitBtn.click(
        user, [user_input, chatbot], [user_input, chatbot], queue=False
    ).then(
        predict,
        [model_name, api_key, chatbot, prompt_input, max_length, top_p, temperature],
        chatbot,
    )
    emptyBtn.click(lambda: (None, None), None, [chatbot, prompt_input], queue=False)
    return (
        chatbot,
        messages,
        dict(
            chat_box=chat_box,
            user_input=user_input,
            submitBtn=submitBtn,
            prompt_input=prompt_input,
            pBtn=pBtn,
            emptyBtn=emptyBtn,
            max_length=max_length,
            top_p=top_p,
            temperature=temperature,
        ),
    )
