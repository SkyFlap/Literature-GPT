import hashlib


def calculate_pdf_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()


# 使用示例
pdf_file = "./examples/examples.pdf"  # 替换为你的PDF文件路径
hash_value = calculate_pdf_hash(pdf_file)
print(f"SHA-256 Hash: {hash_value}")
