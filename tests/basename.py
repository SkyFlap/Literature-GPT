import os


def get_filename_without_extension(path):
    # 获取文件名
    file_name = os.path.basename(path)
    # 去掉后缀名
    file_name_without_extension = os.path.splitext(file_name)[0]
    return file_name_without_extension


# Example usage:
path = "/path/to/file1.json"
file_name = get_filename_without_extension(path)
print(file_name)  # Output should be "file1"
