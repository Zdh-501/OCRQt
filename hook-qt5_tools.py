# hook-qt5_tools.py
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

hiddenimports = collect_submodules('qt5_tools')
datas = collect_data_files('qt5_tools', include_py_files=True)



