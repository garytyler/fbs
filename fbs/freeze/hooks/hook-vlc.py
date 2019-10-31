from PyInstaller.utils.hooks import (
    collect_glib_share_files,
    collect_glib_translations,
    exec_statement,
    get_gi_typelibs,
    collect_dynamic_libs,
    collect_all,
    PY_DYLIB_PATTERNS,
)
from PyInstaller.depend.bindepend import findSystemLibrary
from PyInstaller.compat import is_win, is_darwin, is_unix
from PyInstaller.utils.misc import dlls_in_subdirs
import subprocess

from PyInstaller.depend.bindepend import findSystemLibrary, getfullnameof, findLibrary
from PyInstaller.depend.dylib import include_library
import os
from glob import glob
from importlib import import_module
import sys


def hook(hook_api):
    if not hook_api.__name__ == "vlc":
        return None

    binaries = []

    # vlclib binary
    vlc = import_module("vlc")
    binaries.append((vlc.dll._name, "."))

    vlc_plugin_path = vlc.plugin_path
    vlc_libvlc_path = findSystemLibrary("libvlc")

    # plugin binaries
    for root, _, __ in os.walk(vlc.plugin_path):
        full_paths = []
        for pattern in PY_DYLIB_PATTERNS:
            full_paths.extend(glob(os.path.join(root, pattern)))
        rel_dir = os.path.relpath(root, vlc.plugin_path)
        binaries.extend([(f, rel_dir) for f in full_paths])

    hook_api.add_binaries(binaries)
