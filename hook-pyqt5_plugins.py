# hook-pyqt5_plugins.py
from PyInstaller.utils.hooks import collect_all

datas, binaries, hiddenimports = collect_all('pyqt5_plugins')
