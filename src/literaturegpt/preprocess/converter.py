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
import shutil
from typing import TYPE_CHECKING, Any, Dict, List, Optional
from ..document_loaders.pdf_extract_kit.pdf_extract import pdf_extract_kit
from ..embeddings.zhipu_embedding import zhipu_embedding


def run_con(
    input_folder: str,
    api_key: str,
    embedding_model: str,
    cache_path: str,
    literature_db_path: str,
) -> None:
    literature_db: list = []
    pdf_extract_cache_path = pdf_extract_kit(input_folder, cache_path)
    # pdf_extract_cache_path = ""
    basename = os.path.basename(pdf_extract_cache_path)[0:-5]
    with open(pdf_extract_cache_path, "r", encoding="utf-8") as f:
        extract_info = json.load(f)
    for layout_dets in extract_info:
        literature_db.append(
            {
                "query": layout_dets["layout_dets"],
                "vector": zhipu_embedding(layout_dets["layout_dets"], api_key),
                "page_info": layout_dets["page_info"],
            }
        )
    with open(
        os.path.join(literature_db_path, f"{basename}_db.json"), "w", encoding="utf-8"
    ) as f:
        json.dump(literature_db, f, ensure_ascii=False)
