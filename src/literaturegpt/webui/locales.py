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

LOCALES = {
    "lang": {
        "zh": {
            "label": "语言",
        },
    },
    "model_name": {
        "zh": {
            "label": "模型名称",
        },
    },
    "model_apikey": {
        "zh": {
            "label": "API Key",
            "info": "进行模型身份验证的API Key",
        },
    },
    "embedding_model": {"zh": {"label": "嵌入模型"}},
    "file_upload_check": {"zh": {"value": "文献未上传，请先上传文献。"}},
    "preprocess_button": {"zh": {"value": "文献预处理"}},
    "literature_select_button": {"zh": {"value": "文献选择"}},
    "literature_explorer": {
        "zh": {
            "glob": "*",
            "root_dir": "./literature_db",
            "label": "文献资源管理器",
            "show_label": True,
            "interactive": True,
        }
    },
    "literature_check": {"zh": {"value": "请选择文献"}},
    "qa_mode_button": {"zh": {"value": "问答模式"}},
    "survey_mode_button": {"zh": {"value": "综述模式"}},
    "generate_survey_button": {"zh": {"value": "生成文献综述"}},
    "generate_abstract_button": {"zh": {"value": "生成文献摘要"}},
    "abstract_downloadbutton": {"zh": {"label": "摘要下载"}},
    "survey_downloadbutton": {"zh": {"label": "综述下载"}},
    "load_chat_button": {"zh": {"value": "加载对话界面"}},
}
ALERTS = {
    "file_uploaded": {
        "zh": "文件已上传，可以开始预处理了！",
    },
    "err_file_uploaded": {"zh": "出现错误，请检查文件上传！"},
    "preprocess_check": {"zh": "文献预处理完成！"},
    "err_literature_check": {
        "zh": "文献中存在错误文件，请检查确保勾选文献均为.json格式"
    },
    "literature_check": {"zh": "文献检测完成！"},
    "err_tool_name": {
        "en": "Tool name not found.",
        "ru": "Имя инструмента не найдено.",
        "zh": "工具名称未找到。",
    },
    "err_json_schema": {
        "en": "Invalid JSON schema.",
        "ru": "Неверная схема JSON.",
        "zh": "Json 格式错误。",
    },
}
