import os
import json


def reshape_pdf_info(input_path: str, output_path: str) -> None:
    with open(input_path, "r", encoding="utf-8") as f:
        pdf_info_list = json.load(f)
    base_name = os.path.basename(input_path)
    pdf_extract_db_path = os.path.join(output_path, base_name)
    pdf_reshape_result: list = []
    for pdf_info in pdf_info_list:
        layout_dets: list[dict] = pdf_info["layout_dets"]
        page_info: dict[str, int] = pdf_info["page_info"]
        line_info: str = ""
        for line_dets in layout_dets:
            if line_dets["category_id"] == 13 or line_dets["category_id"] == 14:
                info: str = line_dets["latex"] + "\n"
            elif line_dets["category_id"] == 15:
                info: str = line_dets["text"] + "\n"
            else:
                info = ""
            line_info += info
        pdf_reshape_result.append({"layout_dets": line_info, "page_info": page_info})
    with open(pdf_extract_db_path, "w", encoding="utf-8") as f:
        json.dump(pdf_reshape_result, f, ensure_ascii=False)
    return pdf_extract_db_path


if __name__ == "__main__":
    reshape_pdf_info("src/cache/examples.json", "./")
