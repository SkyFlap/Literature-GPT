from zhipuai import ZhipuAI
import pandas as pd
from ...prompt.prompt import ROLE, SEARCH, SEARCH_FEEDBACK
from ...retrievers.fuzz import find_similar_entries
from ...webui.utils import read_xlsx, parse_key_value


def predict(
    model_name,
    api_key,
    history,
    prompt=ROLE,
    max_length=4096,
    top_p=0.7,
    temperature=0.95,
):
    print(api_key)
    print(model_name)
    messages = []
    print(history)
    if prompt:
        messages.append({"role": "system", "content": prompt})
    for idx, (user_msg, model_msg) in enumerate(history):
        print(f"user_msg:{user_msg}")
        print(f"model_msg:{model_msg}")
        print(f"idx:{idx}")
        print(f"len(history):{len(history)}")
        if prompt and idx == 0:
            pass
        print(2)
        if idx == len(history) - 1 and not model_msg:
            print(1)
            messages.append({"role": "user", "content": user_msg})
            break
        if user_msg:
            messages.append({"role": "user", "content": user_msg})
        if model_msg:
            messages.append({"role": "assistant", "content": model_msg})
    print(messages)
    client = ZhipuAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        max_tokens=max_length,
        top_p=top_p,
        temperature=temperature,
        stream=False,
    )
    feedback = response.choices[0].message.content
    if "查找" in feedback:
        messages = []
        print(history)
        if SEARCH:
            messages.append({"role": "system", "content": SEARCH})
        for idx, (user_msg, model_msg) in enumerate(history):
            if SEARCH and idx == 0:
                pass
            if idx == len(history) - 1 and not model_msg:
                messages.append({"role": "user", "content": user_msg})
                break
            if user_msg:
                messages.append({"role": "user", "content": user_msg})
            if model_msg:
                messages.append({"role": "assistant", "content": model_msg})
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_tokens=max_length,
            top_p=top_p,
            temperature=temperature,
            stream=False,
        )
        feedback = response.choices[0].message.content
        key_value = parse_key_value(feedback)
        df = pd.read_excel("./literature_db/literature_db.xlsx")
        results = find_similar_entries(df, key_value["label"], key_value["value"])
        print(results)
        messages = []
        print(history)
        if SEARCH_FEEDBACK:
            messages.append(
                {
                    "role": "system",
                    "content": SEARCH_FEEDBACK + "\n系统查询信息：\n" + str(results),
                }
            )
        for idx, (user_msg, model_msg) in enumerate(history):
            if SEARCH_FEEDBACK and idx == 0:
                pass
            if idx == len(history) - 1 and not model_msg:
                messages.append({"role": "user", "content": user_msg})
                break
            if user_msg:
                messages.append({"role": "user", "content": user_msg})
            if model_msg:
                messages.append({"role": "assistant", "content": model_msg})
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_tokens=max_length,
            top_p=top_p,
            temperature=temperature,
            stream=True,
        )
    else:
        messages = []
        print(history)
        for idx, (user_msg, model_msg) in enumerate(history):
            if idx == len(history) - 1 and not model_msg:
                messages.append({"role": "user", "content": user_msg})
                break
            if user_msg:
                messages.append({"role": "user", "content": user_msg})
            if model_msg:
                messages.append({"role": "assistant", "content": model_msg})
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_tokens=max_length,
            top_p=top_p,
            temperature=temperature,
            stream=True,
        )
    for chunk in response:
        history[-1][1] += chunk.choices[0].delta.content
        yield history
