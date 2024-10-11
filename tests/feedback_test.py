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
        return {
            "label": label_match.group(1),
            "value": value_match.group(1)
        }
    else:
        return None  # 如果无法解析出有效的键值对，返回None

# 测试用例
input_str = '{\n"label":"你拆解归类的label","value":"你拆解出来的value"\n}'
result = parse_key_value(input_str)
print(result)
