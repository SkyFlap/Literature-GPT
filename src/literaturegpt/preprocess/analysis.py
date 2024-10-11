import os
import json
import re
from zhipuai import ZhipuAI
from ..prompt.surveybot import PROMPT
from ..prompt.prompt import (
    FIRST_LEVEL_CATEGORY,
    CS_SECOND_LEVEL_CATEGORY,
    ECON_SECOND_LEVEL_CATEGORY,
    MGCS_SECOND_LEVEL_CATEGORY,
    THIRD_LEVEL_CATEGORY,
    RESEARCH_METHODS,
    RESEARCH_TOPIC,
    CONTENT_OVERVIEW,
    METODOLOGICAL_ALGORITHMS,
)
from ..webui.utils import write_json_file

category_dict = {
    "计算机科学": CS_SECOND_LEVEL_CATEGORY,
    "经济学": ECON_SECOND_LEVEL_CATEGORY,
    "管理学": MGCS_SECOND_LEVEL_CATEGORY,
}


def match_category(input_str):
    # 尝试解析为严格的JSON格式
    try:
        data = json.loads(input_str)
        if isinstance(data, dict) and "category" in data:
            return {"category": data["category"]}
    except json.JSONDecodeError:
        pass  # 如果解析失败，继续下面的处理
    dict_pattern = r'"category"\s*:\s*"([^"]+)"'
    match = re.search(dict_pattern, input_str)
    if match:
        return {"category": match.group(1)}
    else:
        return None


def match_metodological(input_str):
    # 尝试解析为严格的JSON格式
    try:
        data = json.loads(input_str)
        if isinstance(data, dict) and "metodological" in data:
            return {"metodological": data["metodological"]}
    except json.JSONDecodeError:
        pass  # 如果解析失败，继续下面的处理

    # 使用正则表达式匹配非严格的JSON格式
    list_pattern = r'"metodological"\s*:\s*\[(.*?)\]'
    match = re.search(list_pattern, input_str)
    if match:
        # 提取匹配到的字符串并将其转换为列表
        list_str = match.group(1)
        # 将提取出的字符串按逗号分割，并去掉多余的引号和空格
        result_list = [item.strip().strip('"') for item in list_str.split(',')]
        return {"metodological": result_list}
    else:
        return None


def generate_abstract(api_key: str, model_name: str, file_db_path: str):
    if file_db_path.endswith("json"):
        basename = os.path.basename(file_db_path)
        basename = os.path.splitext(basename)[0]
        with open(file_db_path, "r", encoding="utf-8") as f:
            literature_info = json.load(f)
        if len(literature_info) <= 4:
            for literature_dict in literature_info:
                if literature_dict == literature_info[0]:
                    with open(
                        f"./cache/{basename}_abstract.txt", "a", encoding="utf-8"
                    ) as f:
                        f.write(literature_dict["query"] + "\n")
                messages = []
                messages.append(
                    {"role": "system", "content": PROMPT["analysis_page"]["zh"]}
                )
                messages.append({"role": "user", "content": literature_dict["query"]})
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
            with open(f"./cache/{basename}_abstract.txt", "r", encoding="utf-8") as f:
                page_msg = f.read()
            messages = []
            messages.append(
                {"role": "system", "content": PROMPT["generate_abstract"]["zh"]}
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
            with open(f"./cache/{basename}_abstract.txt", "w", encoding="utf-8") as f:
                f.write(response.choices[0].message.content)
        else:
            for literature_dict in literature_info[0:3]:
                if literature_dict == literature_info[0]:
                    with open(
                        f"./cache/{basename}_abstract.txt", "a", encoding="utf-8"
                    ) as f:
                        f.write(literature_dict["query"] + "\n")
                messages = []
                messages.append(
                    {"role": "system", "content": PROMPT["analysis_page"]["zh"]}
                )
                messages.append({"role": "user", "content": literature_dict["query"]})
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
            with open(f"./cache/{basename}_abstract.txt", "r", encoding="utf-8") as f:
                page_msg = f.read()
            messages = []
            messages.append(
                {"role": "system", "content": PROMPT["generate_abstract"]["zh"]}
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
            with open(f"./cache/{basename}_abstract.txt", "w", encoding="utf-8") as f:
                f.write(response.choices[0].message.content)
    return response.choices[0].message.content


def generate_category(api_key: str, model_name: str, abstract: str):
    messages = []
    messages.append({"role": "system", "content": FIRST_LEVEL_CATEGORY})
    messages.append({"role": "user", "content": abstract})
    client = ZhipuAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        max_tokens=2048,
        top_p=0.7,
        temperature=0.95,
    )
    feedback = match_category(response.choices[0].message.content)
    if feedback:
        first = feedback
        if first in category_dict:
            messages = []
            messages.append({"role": "system", "content": category_dict[first]})
            messages.append({"role": "user", "content": abstract})
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                max_tokens=2048,
                top_p=0.7,
                temperature=0.95,
            )
            feedback = match_category(response.choices[0].message.content)
            if feedback:
                second = feedback
            else:
                second = "其他"
            messages = []
            messages.append({"role": "system", "content": THIRD_LEVEL_CATEGORY})
            messages.append(
                {
                    "role": "user",
                    "content": f"一级研究方向分类:\n{first}\n二级研究方向分类:\n{second}\n摘要：\n{abstract}",
                }
            )
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                max_tokens=2048,
                top_p=0.7,
                temperature=0.95,
            )
            feedback = match_category(response.choices[0].message.content)
            if feedback:
                third = feedback
            else:
                third = "其他"
    else:
        first, second, third = "其他", "其他", "其他"

    return first, second, third


def generate_research_methods(api_key: str, model_name: str, abstract: str):
    messages = []
    messages.append({"role": "system", "content": RESEARCH_METHODS})
    messages.append({"role": "user", "content": f"摘要：{abstract}"})
    client = ZhipuAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        max_tokens=2048,
        top_p=0.7,
        temperature=0.95,
    )
    if response.choices[0].message.content:
        return response.choices[0].message.content
    else:
        return ""


def generate_research_topic(api_key: str, model_name: str, abstract: str):
    messages = []
    messages.append({"role": "system", "content": RESEARCH_TOPIC})
    messages.append({"role": "user", "content": f"摘要：{abstract}"})
    client = ZhipuAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        max_tokens=2048,
        top_p=0.7,
        temperature=0.95,
    )
    if response.choices[0].message.content:
        return response.choices[0].message.content
    else:
        return ""


def genreate_content_overview(api_key: str, model_name: str, abstract: str):
    messages = []
    messages.append({"role": "system", "content": CONTENT_OVERVIEW})
    messages.append({"role": "user", "content": f"摘要：{abstract}"})
    client = ZhipuAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        max_tokens=2048,
        top_p=0.7,
        temperature=0.95,
    )
    if response.choices[0].message.content:
        return response.choices[0].message.content
    else:
        return ""


def generate_measurement_methods():
    pass


def generate_methodological_algorithms(api_key: str, model_name: str, abstract: str):
    messages = []
    messages.append({"role": "system", "content": METODOLOGICAL_ALGORITHMS})
    messages.append({"role": "user", "content": f"摘要：{abstract}"})
    client = ZhipuAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        max_tokens=2048,
        top_p=0.7,
        temperature=0.95,
    )
    feedback = match_metodological(response.choices[0].message.content)
    if feedback:
        return str(feedback)
    else:
        return ""


def run_analysis(
    api_key: str, model_name: str, file_db_path: str, literature_db_path: str
):
    """需要获取研究内容（摘要）、一级研究方向、二级研究方向、三级研究方向、研究方法、研究主题、内容概述、测度方法、方法算法"""
    abstract = generate_abstract(api_key, model_name, file_db_path)
    first, second, third = generate_category(api_key, model_name, abstract)
    research_methods = generate_research_methods(api_key, model_name, abstract)
    research_topic = generate_research_topic(api_key, model_name, abstract)
    content_overview = genreate_content_overview(api_key, model_name, abstract)
    # generate_measurement_methods()
    methodological_algorithms = generate_methodological_algorithms(
        api_key, model_name, abstract
    )

    return (
        abstract,
        first,
        second,
        third,
        research_methods,
        research_topic,
        content_overview,
        methodological_algorithms,
    )
