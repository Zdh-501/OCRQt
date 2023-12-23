import subprocess
import os

# 指定你的主程序文件名
main_script = 'MainWindow.py'

# 指定打包后的程序名称
name = 'YourApplication'

# 为 PyInstaller 构建命令
pyinstaller_command = [
    'pyinstaller',
    '--noconfirm',
    '--onedir',
    '--windowed',
    '--name', name,
    '--add-data', 'ui/impl/*;ui/impl/',
    '--add-data', 'ui/layout/*;ui/layout/',
    '--add-data', 'ui/pic/*;ui/pic/',
    '--add-data', 'SQL/*;SQL/',
    '--add-data', 'config.json;.',
    '--add-data', 'PaddleOCR/*;PaddleOCR/',
    main_script
]

# 运行命令
subprocess.run(pyinstaller_command, shell=True)
