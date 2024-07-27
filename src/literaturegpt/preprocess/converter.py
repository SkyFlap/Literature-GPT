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
import shutil
from typing import TYPE_CHECKING, Any, Dict, List, Optional
from ..document_loaders.pdf_extract_kit.pdf_extract import pdf_extract_kit


def run_con(input_folder: str, output_folder: str) -> None:
    pdf_extract_kit(input_folder, output_folder)
