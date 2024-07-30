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
import json
from copy import deepcopy
from subprocess import Popen, TimeoutExpired
from typing import TYPE_CHECKING, Any, Dict, List, Generator, Optional
from ..extras.packages import is_gradio_available
from .locales import ALERTS
from ..preprocess.converter import run_con
from .components.chatbot import predict, parse_text
from ..prompt.surveybot import PROMPT
from ..retrievers.hybrid_search import hybrid_search

if is_gradio_available():
    import gradio as gr


from gradio.components import Component
from .manager import Manager


class Runner:
    def __init__(self, manager: "Manager", demo_mode: bool = False) -> None:
        self.manager = manager
        self.demo_mode = demo_mode
        """ Resume """
        self.trainer: Optional["Popen"] = None
        self.do_train = True
        self.running_data: Dict["Component", Any] = None
        """ State """
        self.aborted = False
        self.running = False

    def check_file(self, data: Dict["Component", Any]) -> str:
        get = lambda elem_id: data[self.manager.get_elem_by_id(elem_id)]
        lang, file_list = get("top.lang"), get("preprocess.file_upload")
        return (
            ALERTS["file_uploaded"][lang]
            if file_list != None
            else ALERTS["err_file_uploaded"][lang]
        )

    def get_base_info(self, data: Dict["Component", Any]):
        get = lambda elem_id: data[self.manager.get_elem_by_id(elem_id)]
        lang, model_name, api_key = (
            get("top.lang"),
            get("top.model_name"),
            get("top.model_apikey"),
        )
        return lang, model_name, api_key

    def run_preprocess(self, data: Dict["Component", Any]):
        get = lambda elem_id: data[self.manager.get_elem_by_id(elem_id)]
        lang, api_key, embedding_model, file_list = (
            get("top.lang"),
            get("top.model_apikey"),
            get("preprocess.embedding_model"),
            get("preprocess.file_upload"),
        )
        cache_path = "./cache"
        db_path = "./literature_db"
        for file in file_list:
            run_con(file, api_key, embedding_model, cache_path, db_path)
        return ALERTS["preprocess_check"][lang]

    def literature_check(self, data: Dict["Component", Any]):
        get = lambda elem_id: data[self.manager.get_elem_by_id(elem_id)]
        lang, literature_explorer = get("top.lang"), get(
            "literature.literature_explorer"
        )
        for path in literature_explorer:
            if os.path.isdir(path):
                # It's a directory, continue checking other paths
                continue
            elif os.path.isfile(path):
                # It's a file, check if it ends with .json
                if not path.endswith(".json"):
                    return ALERTS["err_literature_check"][lang]
            else:
                # It's neither a file nor a directory, return False
                return ALERTS["err_literature_check"][lang]
        return ALERTS["literature_check"][lang]

    def generate_survey(self, data: Dict["Component", Any]):
        get = lambda elem_id: data[self.manager.get_elem_by_id(elem_id)]
        lang, model_name, api_key, literature_explorer = (
            get("top.lang"),
            get("top.model_name"),
            get("top.model_apikey"),
            get("literature.literature_explorer"),
        )
        survey_messages = []
        survey_query = ""
        for literature in literature_explorer:
            literature: str
            if literature.endswith("json"):
                basename = os.path.basename(literature)
                basename = os.path.splitext(basename)[0]
                with open(literature, "r", encoding="utf-8") as f:
                    literature_info = json.load(f)
                for literature_dict in literature_info:
                    if literature_dict == literature_info[0]:
                        with open(
                            f"./cache/{basename}_abstract.txt", "a", encoding="utf-8"
                        ) as f:
                            f.write(literature_dict["query"] + "\n")
                    from zhipuai import ZhipuAI

                    messages = []
                    messages.append(
                        {"role": "system", "content": PROMPT["analysis_page"][lang]}
                    )
                    messages.append(
                        {"role": "user", "content": literature_dict["query"]}
                    )
                    client = ZhipuAI(api_key=api_key)
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=messages,
                        max_tokens=1024,
                        top_p=0.7,
                        temperature=0.95,
                    )
                    with open(
                        f"./cache/{basename}_abstract.txt", "a", encoding="utf-8"
                    ) as f:
                        f.write(response.choices[0].message.content)
                with open(
                    f"./cache/{basename}_abstract.txt", "r", encoding="utf-8"
                ) as f:
                    page_msg = f.read()
                    messages = []
                    messages.append(
                        {"role": "system", "content": PROMPT["generate_abstract"][lang]}
                    )
                    messages.append({"role": "user", "content": page_msg})
                    client = ZhipuAI(api_key=api_key)
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=messages,
                        max_tokens=2048,
                        top_p=0.7,
                        temperature=0.95,
                    )
                    with open(
                        f"./cache/{basename}_abstract.txt", "w", encoding="utf-8"
                    ) as f:
                        f.write(response.choices[0].message.content)
                    survey_query += response.choices[0].message.content
        survey_messages.append(
            {"role": "system", "content": PROMPT["generate_survey"][lang]}
        )
        survey_messages.append({"role": "user", "content": survey_query})
        client = ZhipuAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_tokens=1024,
            top_p=0.7,
            temperature=0.95,
        )
        from datetime import datetime

        current_time = (
            (str(datetime.now())).replace("-", "_").replace(" ", "_").replace(":", "_")
        )
        with open(f"./cache/{current_time}_abstract.txt", "w", encoding="utf-8") as f:
            f.write(survey_query)
        with open(f"./cache/{current_time}_survey.txt", "w", encoding="utf-8") as f:
            f.write(response.choices[0].message.content)
        return [
            response.choices[0].message.content,
            gr.DownloadButton(
                label="Download abstract",
                value=f"./cache/{current_time}_abstract.txt",
                visible=True,
            ),
            gr.DownloadButton(
                label="Download survey",
                value=f"./cache/{current_time}_survey.txt",
                visible=True,
            ),
        ]

    def generate_abstract(self, data: Dict["Component", Any]):
        get = lambda elem_id: data[self.manager.get_elem_by_id(elem_id)]
        lang, model_name, api_key, literature_explorer = (
            get("top.lang"),
            get("top.model_name"),
            get("top.model_apikey"),
            get("literature.literature_explorer"),
        )
        survey_query = ""
        for literature in literature_explorer:
            literature: str
            if literature.endswith("json"):
                basename = os.path.basename(literature)
                basename = os.path.splitext(basename)[0]
                with open(literature, "r", encoding="utf-8") as f:
                    literature_info = json.load(f)
                for literature_dict in literature_info:
                    if literature_dict == literature_info[0]:
                        with open(
                            f"./cache/{basename}_abstract.txt", "a", encoding="utf-8"
                        ) as f:
                            f.write(literature_dict["query"] + "\n")
                    from zhipuai import ZhipuAI

                    messages = []
                    messages.append(
                        {"role": "system", "content": PROMPT["analysis_page"][lang]}
                    )
                    messages.append(
                        {"role": "user", "content": literature_dict["query"]}
                    )
                    client = ZhipuAI(api_key=api_key)
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=messages,
                        max_tokens=1024,
                        top_p=0.7,
                        temperature=0.95,
                    )
                    with open(
                        f"./cache/{basename}_abstract.txt", "a", encoding="utf-8"
                    ) as f:
                        f.write(response.choices[0].message.content)
                with open(
                    f"./cache/{basename}_abstract.txt", "r", encoding="utf-8"
                ) as f:
                    page_msg = f.read()
                    messages = []
                    messages.append(
                        {"role": "system", "content": PROMPT["generate_abstract"][lang]}
                    )
                    messages.append({"role": "user", "content": page_msg})
                    client = ZhipuAI(api_key=api_key)
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=messages,
                        max_tokens=2048,
                        top_p=0.7,
                        temperature=0.95,
                    )
                    with open(
                        f"./cache/{basename}_abstract.txt", "w", encoding="utf-8"
                    ) as f:
                        f.write(response.choices[0].message.content)
                    survey_query += response.choices[0].message.content
        from datetime import datetime

        current_time = (
            (str(datetime.now())).replace("-", "_").replace(" ", "_").replace(":", "_")
        )
        with open(f"./cache/{current_time}_abstract.txt", "w", encoding="utf-8") as f:
            f.write(survey_query)
        return [
            response.choices[0].message.content,
            gr.DownloadButton(
                label="Download abstract",
                value=f"./cache/{current_time}_abstract.txt",
                visible=True,
            ),
        ]
