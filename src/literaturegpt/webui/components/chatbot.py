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
from ..utils import check_json_schema, get_file_content, parse_text
from ...model.llm.zhipu import predict

if is_gradio_available():
    import gradio as gr

latex_delimiters_set = [
    {"left": "$$", "right": "$$", "display": True},
    {"left": "$", "right": "$", "display": False},
    {"left": "\\(", "right": "\\)", "display": False},
    {"left": "\\[", "right": "\\]", "display": True},
    {"left": "\\begin{equation}", "right": "\\end{equation}", "display": True},
    {"left": "\\begin{align}", "right": "\\end{align}", "display": True},
    {"left": "\\begin{alignat}", "right": "\\end{alignat}", "display": True},
    {"left": "\\begin{gather}", "right": "\\end{gather}", "display": True},
    {"left": "\\begin{CD}", "right": "\\end{CD}", "display": True},
]


def create_file_box(
    engine: "Engine", visible: bool = False
) -> Tuple["Component", "Component", Dict[str, "Component"]]:
    model_name, api_key = engine.manager.get_elem_by_id(
        "top.model_name"
    ), engine.manager.get_elem_by_id("top.model_apikey")


def create_chat_box(
    engine: "Engine", visible: bool = False
) -> Tuple["Component", "Component", Dict[str, "Component"]]:
    model_name, api_key = engine.manager.get_elem_by_id(
        "top.model_name"
    ), engine.manager.get_elem_by_id("top.model_apikey")
    with gr.Column(visible=visible) as chat_box:
        with gr.Row():
            chatbot = gr.Chatbot(
            latex_delimiters=latex_delimiters_set,
            sanitize_html=False,
            # height=700,
            show_label=False,
            avatar_images=[
                "./literaturegpt/resources/img/user.png",
                "./literaturegpt/resources/img/openai-black.png",
            ],
            show_share_button=False,
            placeholder=get_file_content(
                "./literaturegpt/resources/md/chatbot_placeholder.md"
            ),
        )
            file_download_box = gr.Files(visible=False)
        messages = gr.State([])
        with gr.Row():
            file_upload_box = gr.File()
            user_input = gr.Textbox(
                show_label=False,
                placeholder="在这里输入",
                lines=10,
                max_lines=20,
                min_width=420,
                scale=12,
            )
            submitBtn = gr.Button(variant="primary", scale=1)
            emptyBtn = gr.Button(variant="secondary", scale=1)

    def user(query, history):
        return "", history + [[parse_text(query), ""]], gr.Files(visible=False)

    submitBtn.click(
        user,
        [user_input, chatbot],
        [user_input, chatbot, file_download_box],
        queue=False,
    ).then(
        predict,
        [model_name, api_key, chatbot],
        chatbot,
    )
    emptyBtn.click(lambda: None, None, [chatbot], queue=False)
    return (
        chatbot,
        messages,
        dict(
            chat_box=chat_box,
            user_input=user_input,
            submitBtn=submitBtn,
            emptyBtn=emptyBtn,
            file_download_box=file_download_box,file_upload_box=file_upload_box
        ),
    )
