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
import os
import signal
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import psutil
from transformers.trainer_utils import get_last_checkpoint
from yaml import safe_dump, safe_load


def get_time() -> str:
    r"""
    Gets current date and time.
    """
    return datetime.now().strftime(r"%Y-%m-%d-%H-%M-%S")



