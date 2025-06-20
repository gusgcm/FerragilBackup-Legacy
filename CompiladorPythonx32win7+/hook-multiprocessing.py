# Hook vazio para excluir multiprocessing
from PyInstaller.utils.hooks import collect_submodules
hiddenimports = []
excludes = ['multiprocessing']
