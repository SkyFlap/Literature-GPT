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
import pandas as pd
import os
import openpyxl
import hashlib
import signal
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import psutil
from transformers.trainer_utils import get_last_checkpoint
from yaml import safe_dump, safe_load

from ..extras.packages import is_gradio_available
from .common import DEFAULT_CACHE_DIR, DEFAULT_CONFIG_DIR
from .locales import ALERTS


if is_gradio_available():
    import gradio as gr


def get_time() -> str:
    r"""
    Gets current date and time.
    """
    return datetime.now().strftime(r"%Y-%m-%d-%H-%M-%S")


def check_json_schema(text: str, lang: str) -> None:
    r"""
    Checks if the json schema is valid.
    """
    try:
        tools = json.loads(text)
        if tools:
            assert isinstance(tools, list)
            for tool in tools:
                if "name" not in tool:
                    raise NotImplementedError("Name not found.")
    except NotImplementedError:
        gr.Warning(ALERTS["err_tool_name"][lang])
    except Exception:
        gr.Warning(ALERTS["err_json_schema"][lang])


def read_csv(file_path: str) -> pd.DataFrame:
    try:
        # 读取 CSV 文件，空单元格替换为 ""
        df = pd.read_csv(file_path, dtype=str, na_filter=False)
        df.fillna("", inplace=True)  # 用空字符串替换 NaN
        return df
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
        return None


def read_xlsx(file_path: str) -> pd.DataFrame:
    try:
        # 读取 Excel 文件，空单元格替换为 ""
        df = pd.read_excel(file_path, dtype=str, na_filter=False)
        df.fillna("", inplace=True)  # 用空字符串替换 NaN
        return df
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
        return None


def get_file_content(path: str) -> str:
    if os.path.exists(path):
        with open(path, encoding="utf8") as file:
            return file.read()
    return ""


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


def calculate_pdf_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()


import re
import json


def parse_key_value(input_str):
    # 尝试解析为严格的JSON格式
    try:
        data = json.loads(input_str)
        if isinstance(data, dict) and "label" in data and "value" in data:
            return {"label": data["label"], "value": data["value"]}
    except json.JSONDecodeError:
        pass  # 如果解析失败，继续下面的处理

    # 使用正则表达式提取label和value的值
    label_pattern = r'"label"\s*:\s*"([^"]+)"'
    value_pattern = r'"value"\s*:\s*"([^"]+)"'

    label_match = re.search(label_pattern, input_str)
    value_match = re.search(value_pattern, input_str)

    # 确保两者都匹配到
    if label_match and value_match:
        return {"label": label_match.group(1), "value": value_match.group(1)}
    else:
        return None  # 如果无法解析出有效的键值对，返回None


def write_json_file(data, file_path):
    """
    将数据写入指定路径的 JSON 文件。

    参数:
    data: 要写入 JSON 文件的数据 (通常是字典或列表)。
    file_path: 文件路径 (包括文件名)。
    """
    try:
        # 使用 with 自动管理文件关闭
        with open(file_path, "w", encoding="utf-8") as json_file:
            # 将数据以 JSON 格式写入文件
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"数据成功写入 {file_path}")
    except Exception as e:
        print(f"写入文件时出错: {e}")


def append_dict_to_excel(dict_data, excel_path):
    # Load the workbook and active sheet
    wb = openpyxl.load_workbook(excel_path)
    sheet = wb.active

    # Get the header from the first row
    headers = [cell.value for cell in sheet[1]]

    # Create a list for the new row based on dict_data
    new_row = []
    for header in headers:
        # Match the dict keys to headers, fill with empty string if key is missing
        value = dict_data.get(header, "")
        new_row.append(str(value))  # Convert to string

    # Append the new row to the sheet
    sheet.append(new_row)

    # Save the workbook back to the file
    wb.save(excel_path)
