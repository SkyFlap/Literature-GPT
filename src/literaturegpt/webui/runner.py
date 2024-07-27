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
from copy import deepcopy
from subprocess import Popen, TimeoutExpired
from typing import TYPE_CHECKING, Any, Dict, List, Generator, Optional
from ..extras.packages import is_gradio_available
from .locales import ALERTS
from ..preprocess.converter import run_con

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

    def check_file(self, lang, file_list: list) -> str:
        print(f"lang:{lang}")
        print(file_list)
        return (
            ALERTS["file_uploaded"][lang]
            if file_list != None
            else ALERTS["err_file_uploaded"][lang]
        )

    def run_preprocess(self, lang, file_list: list):
        cache_path = "./cache"
        for file in file_list:
            run_con(file, cache_path)
        return ALERTS["preprocess_check"][lang]
