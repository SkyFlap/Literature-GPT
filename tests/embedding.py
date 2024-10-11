import os
import json


def zhipu_embedding(query: str, api_key: str) -> list[int]:
    from zhipuai import ZhipuAI

    client = ZhipuAI(api_key=api_key)
    response = client.embeddings.create(
        model="embedding-2",
        input=query,
    )
    return response.data[0].embedding


api_key = ""
literature_db: list = []
literature_db_path = "./"
pdf_extract_cache_path = "src/cache/examples_reshape.json"
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
    page_num = layout_dets["page_info"]["page_no"]
    print(f"processed page {page_num}")
with open(
    os.path.join(literature_db_path, f"{basename}_db.json"), "w", encoding="utf-8"
) as f:
    json.dump(literature_db, f, ensure_ascii=False)
