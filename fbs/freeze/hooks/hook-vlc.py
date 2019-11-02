import os
from os.path import join, dirname, relpath, commonpath
from glob import glob
from importlib import import_module

from PyInstaller.compat import is_darwin, is_win, is_linux
from PyInstaller.depend.bindepend import findSystemLibrary
from PyInstaller.utils.hooks import get_homebrew_path

PY_DYLIB_PATTERNS = ["*.dylib"]

def hook(hook_api):
    if not hook_api.__name__ == "vlc":
        return None

    libvlc_src_file = os.environ["PYTHON_VLC_LIB_PATH"]
    plugin_src_dir = os.environ["PYTHON_VLC_MODULE_PATH"]

    # Get common root
    common_root = commonpath([libvlc_src_file, plugin_src_dir])

    # Add libvlc binaries
    libvlc_src_files = glob(join(dirname(libvlc_src_file), '*.dylib'))
    libvlc_binaries = []
    for f in libvlc_src_files:
        binary_tuple = (f, ".")
        libvlc_binaries.append(binary_tuple)
    hook_api.add_binaries(libvlc_binaries)

    # Add plugin binaries
    plugin_src_files = []
    for root, _, __ in os.walk(plugin_src_dir):
        for pattern in PY_DYLIB_PATTERNS:
            plugin_src_files.extend(glob(join(root, pattern)))
    plugin_binaries = []
    for f in plugin_src_files:
        rel_dir = relpath(dirname(f), common_root)
        bin_tuple = (f, rel_dir)
        plugin_binaries.append(bin_tuple)
    hook_api.add_binaries(plugin_binaries)
