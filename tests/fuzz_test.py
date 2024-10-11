from fuzzywuzzy import fuzz
import pandas as pd


def find_similar_entries(
    df: pd.DataFrame, label: str, value: str, top_n: int = 10
) -> list:
    if label not in df.columns:
        print(f"标签 '{label}' 不存在")
        return []

    # 计算相似度并添加到 DataFrame
    df["similarity"] = df[label].apply(lambda x: fuzz.ratio(x, value))

    # 根据相似度排序并选择前 top_n 个
    top_entries = df.nlargest(top_n, "similarity")

    # 返回相关列的前 top_n 条数据，转换为字典列表
    result = top_entries.drop(columns=["similarity"]).to_dict(orient="records")

    return result

df = pd.read_excel(r'src\literature_db\literature_db.xlsx')
results = find_similar_entries(df, '二级研究方向', '深度学习')
print(results)