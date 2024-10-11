import json
import os
from zhipuai import ZhipuAI
from typing import TYPE_CHECKING, Dict, Generator, List, Optional, Sequence, Tuple, Any
from numpy.typing import NDArray
from ..data import Role
from ..extras.packages import is_gradio_available
from .locales import ALERTS
from ..prompt.qabot import PROMPT
from ..retrievers.hybrid_search import hybrid_search

if TYPE_CHECKING:
    from .manager import Manager


if is_gradio_available():
    import gradio as gr
from gradio.components import Component


class WebChatModel:
    def __init__(self, manager: "Manager") -> None:
        self.manager = manager

    def stream(self, data: Dict["Component", Any]):
        get = lambda elem_id: data[self.manager.get_elem_by_id(elem_id)]
        (
            lang,
            model_name,
            api_key,
            literature_explorer,
            top_p,
            max_length,
            temperature,
            history,
            user_qainput,
        ) = (
            get("top.lang"),
            get("top.model_name"),
            get("top.model_apikey"),
            get("literature.literature_explorer"),
            get("literature.top_p"),
            get("literature.max_length"),
            get("literature.temperature"),
            get("literature.qabot"),
            get("literature.user_qainput"),
        )
        print(f"history:{history}")
        print(f"user_qainput:{user_qainput}")
        messages: list = []
        pre_messages: list = []
        db_embedding_vectors: list = []
        prompt = PROMPT["qa_prompt"][lang]
        pre_messages.append({"role": "system", "content": PROMPT["extract_key"][lang]})
        for idx, (user_msg, model_msg) in enumerate(history):
            print(f"idx:{idx}")
            print(len(history))
            print(f"user_msg:{user_msg}")
            print(f"model_msg:{model_msg}")
            if user_msg == history[-1][0]:
                pre_messages.append({"role": "user", "content": user_msg})
                break
        client = ZhipuAI(api_key=api_key)
        print(f"pre_messages:{pre_messages}")
        response = client.chat.completions.create(
            model=model_name,
            messages=pre_messages,
            max_tokens=max_length,
            top_p=top_p,
            temperature=temperature,
        )
        print(response)
        query_embedding_vector = client.embeddings.create(
            model="embedding-2",
            input=response.choices[0].message.content,
        )
        query_embedding_vector = query_embedding_vector.data[0].embedding
        with open(literature_explorer[0], "r", encoding="utf-8") as f:
            literature_db = json.load(f)
        for literature_dict in literature_db:
            db_embedding_vectors.append(literature_dict["vector"])
        index = hybrid_search(
            query_embedding_vector=query_embedding_vector,
            db_embedding_vectors=db_embedding_vectors,
            n=2,
        )
        print(index)
        kg_db = ""
        for idx in index:
            kg_db += literature_db[idx]["query"]
        if prompt:
            messages.append({"role": "system", "content": prompt})
        for idx, (user_msg, model_msg) in enumerate(history):
            print(f"idx:{idx}")
            print(len(history))
            print(f"user_msg:{user_msg}")
            print(f"model_msg:{model_msg}")
            if user_msg == history[-1][0]:
                messages.append(
                    {
                        "role": "user",
                        "content": f"## Userinput:\n{user_msg}\n## 知识库内容\n{kg_db}",
                    }
                )
                break
            if user_msg:
                messages.append({"role": "user", "content": user_msg})
            if model_msg:
                messages.append({"role": "assistant", "content": model_msg})
        client = ZhipuAI(api_key=api_key)
        print(messages)
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_tokens=max_length,
            top_p=top_p,
            temperature=temperature,
        )
        history[-1][1] += response.choices[0].message.content
        return history
