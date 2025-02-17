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


from collections import OrderedDict, defaultdict
from enum import Enum
from typing import Dict, Optional

SUPPORTED_MODELS = ["glm-4-0520", "glm-4", "glm-4-air", "glm-4-airx", "glm-4-flash"]


class ClientSource(str, Enum):
    base_url = "hf"
