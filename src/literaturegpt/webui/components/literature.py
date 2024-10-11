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

import pandas as pd
from typing import TYPE_CHECKING, Dict, Tuple

if TYPE_CHECKING:
    from gradio.components import Component

    from ..engine import Engine
from ..utils import read_csv, read_xlsx
from ...extras.packages import is_gradio_available


if is_gradio_available():
    import gradio as gr


def creat_literature_db(
    engine: "Engine", visible: bool = False
) -> Tuple["Component", "Component", Dict[str, "Component"]]:
    literature_database = read_xlsx("./literature_db/literature_db.xlsx")
    if literature_database is None or literature_database.empty:
        print("数据读取失败或文件为空")
        return None, None
    first_row = literature_database.iloc[0].tolist()
    data_from_second_row = literature_database.iloc[0:].reset_index(drop=True)
    with gr.Column(visible=visible) as db_box:
        literature_table = gr.Dataframe(
            value=data_from_second_row,
            headers=first_row,
            column_widths="10%"
        )
    return literature_table, dict(db_box=db_box)


def create_literature_tab(engine: "Engine") -> Dict[str, "Component"]:
    input_elems = engine.manager.get_base_elems()
    elem_dict = dict()
    literature_load_btn = gr.Button()
    literature_view_btn = gr.Button()
    literature_select_btn = gr.Button()
    with gr.Row():
        literature_explorer = gr.FileExplorer(
            height=500,
            glob="*",
            root_dir="./output",
            interactive=True,
            show_label=True,
            label="文献资源管理器",
        )
        literature_content_view = gr.Code(lines=30, scale=2, language="json")
    input_elems.update({literature_load_btn})
    literature_table, db_elems = creat_literature_db(engine, visible=False)
    elem_dict.update(
        dict(
            literature_view_btn=literature_view_btn,
            literature_select_btn=literature_select_btn,
            literature_table=literature_table,
            literature_explorer=literature_explorer,
            literature_content_view=literature_content_view,
            literature_load_btn=literature_load_btn,
        )
    )
    elem_dict.update(db_elems)

    def vile_file(file):
        if len(file) == 1:
            return (file[0],)
        elif len(file) == 0:
            gr.Warning("请选择一个文件")
        else:
            gr.Warning("仅能选择一个文件")

    literature_view_btn.click(vile_file, literature_explorer, literature_content_view)
    literature_load_btn.click(
        lambda: gr.Column(visible=True),
        outputs=[db_elems["db_box"]],
    )
    return elem_dict
