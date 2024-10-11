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
from collections import defaultdict
from typing import Any, Dict, Optional, Tuple

from yaml import safe_dump, safe_load

from ..extras.logging import get_logger
from ..extras.packages import is_gradio_available


if is_gradio_available():
    import gradio as gr


logger = get_logger(__name__)


DEFAULT_CACHE_DIR = "cache"
DEFAULT_CONFIG_DIR = "config"
DEFAULT_DATA_DIR = "data"
DEFAULT_SAVE_DIR = "saves"
USER_CONFIG = "user_config.yaml"


def get_config_path() -> os.PathLike:
    r"""
    Gets the path to user config.
    """
    return os.path.join(DEFAULT_CACHE_DIR, USER_CONFIG)


def load_config() -> Dict[str, Any]:
    r"""
    Loads user config if exists.
    """
    try:
        with open(get_config_path(), "r", encoding="utf-8") as f:
            return safe_load(f)
    except Exception:
        return {"lang": None, "last_model": None, "api_key": {}, "cache_dir": None}


def save_config(
    lang: str, model_name: Optional[str] = None, api_key: Optional[str] = None
) -> None:
    r"""
    Saves user config.
    """
    os.makedirs(DEFAULT_CACHE_DIR, exist_ok=True)
    user_config = load_config()
    user_config["lang"] = lang or user_config["lang"]
    if model_name:
        user_config["last_model"] = model_name

    if model_name and api_key:
        user_config["api_key"][model_name] = api_key

    with open(get_config_path(), "w", encoding="utf-8") as f:
        safe_dump(user_config, f)
