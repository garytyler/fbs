import os
from os.path import join, dirname, relpath, commonpath, abspath
from glob import glob
from importlib import import_module
from PyInstaller.compat import is_darwin, is_win, is_linux


if is_linux:
    DYLIB_PATTERN = "lib*.so"
elif is_win:
    DYLIB_PATTERN = "*.dll"
elif is_darwin:
    DYLIB_PATTERN = "*.dylib"


def hook(hook_api):
    if not hook_api.__name__ == "vlc":
        return None

    libvlc_src_file = abspath(os.environ["PYTHON_VLC_LIB_PATH"])
    plugin_src_dir = abspath(os.environ["PYTHON_VLC_MODULE_PATH"])

    # Add libvlc binaries
    libvlc_src_files = glob(join(dirname(libvlc_src_file), DYLIB_PATTERN))
    libvlc_binaries = []
    for f in libvlc_src_files:
        binary_tuple = (f, ".")
        libvlc_binaries.append(binary_tuple)
    hook_api.add_binaries(libvlc_binaries)

    # Add plugin binaries
    plugin_src_files = []
    for root, _, __ in os.walk(plugin_src_dir):
        pattern = join(root, DYLIB_PATTERN)
        plugin_src_files.extend(glob(pattern))

    # print(plugin_src_files)
    plugin_binaries = []
    for f in plugin_src_files:
        src_plugins_root = f
        while not src_plugins_root.endswith("plugins"):
            src_plugins_root = dirname(src_plugins_root)
        dst_rel_dir = join("plugins", relpath(f, src_plugins_root))
        binary_tuple = (f, dst_rel_dir)
        plugin_binaries.append(binary_tuple)
    hook_api.add_binaries(plugin_binaries)