@echo off
setlocal enabledelayedexpansion

rem 获取当前批处理文件所在的目录路径
set "project_dir=%~dp0"

rem 删除__pycache__文件夹
for /d /r "%project_dir%" %%d in (__pycache__) do (
    echo Deleting folder: %%d
    rd /s /q "%%d"
)

echo All __pycache__ folders deleted.

pause
