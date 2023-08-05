# -*- coding:utf-8 -*-

import six
import os
import re
import glob
import shutil
from krux.regex import grep, simple_pattern_to_regex
from krux.converters.string_related import dict2str

from ..fsmod import FSMod
from ..path import *
from .utils import *
from .list_file import *


__all__ = ['LocalFSMod']


class LocalFSMod(FSMod):
    schema = None
    name = 'local'

    def ls(self, root=None, **kwargs):
        return LS(root=root, **kwargs)

    def ls_grep(self, root=None, pattern=None, **kwargs):
        return LS_GREP(root=root, pattern=pattern, **kwargs)

    def ls_group(self, root=None, pattern=None, **kwargs):
        return LS_GROUP(root=root, pattern=pattern, **kwargs)

    def exists(self, path):
        return os.path.exists(path)

    def mkdir(self, dir_path, force=False):
        #TODO: make it more robust
        if dir_path in ['', '.', '..', './', '../', '/']:
            return
        orig = dir_path
        if is_link(orig):
            orig = find_link_orig(dir_path)
        if is_file(orig):
            if not force:
                raise RuntimeError('Cannot makedir: %s is file' % dir_path)
        if force:
            try:
                self.rm(dir_path)
            except Exception as e:
                pass
        try:
            os.makedirs(dir_path)
        except OSError as e:
            if e.errno != 17:
                raise e

    def rm(self, path):
        if path in ['/', '/*']:
            return

        fnames = glob.glob(path)
        for fn in fnames:
            try:
                self._rm_one_file(fn)
            except Exception as e:
                six.print_(e)

    def _rm_one_file(self, path):
        if is_link(path):
            os.unlink(path)
        elif is_dir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

    def du(self, path):
        """disk usage
        part of this code comes from monkut (http://stackoverflow.com/questions/1392413/calculating-a-directory-size-using-python)
        """
        total_size = 0
        if is_dir(path):
            for dirpath, dirnames, filenames in os.walk(path):
                total_size += os.path.getsize(dirpath)
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    total_size += os.path.getsize(fp)
        else:
            total_size = os.path.getsize(path)
        return total_size
