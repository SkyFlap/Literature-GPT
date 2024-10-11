from fuzzywuzzy import fuzz
import pandas as pd


def find_similar_entries(
    df: pd.DataFrame, label: str, value: str, top_n: int = 5
) -> list:
    print(f"查询label:{label},value:{value}")
    if label not in df.columns:
        print(f"标签 '{label}' 不存在")
        return []

    # 计算相似度并添加到 DataFrame
    df["similarity"] = df[label].apply(
        lambda x: fuzz.ratio(str(x), str(value)) if pd.notnull(x) else 0
    )

    # 根据相似度排序并选择前 top_n 个
    top_entries = df.nlargest(top_n, "similarity")

    # 返回相关列的前 top_n 条数据，转换为字典列表
    result = top_entries.drop(columns=["similarity"]).to_dict(orient="records")

    return result
