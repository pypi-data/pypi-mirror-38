# -*- coding: utf-8 -*-

import os
import subprocess
import sys


def ispy(file):
    return (os.path.isfile(file) and (os.path.splitext(file)[1] == '.py'))


for file in filter(ispy, os.listdir('.')):
    if file == __file__:
        continue

    stem, ext = os.path.splitext(file)
    name = '%s.pyw' % stem

    new = subprocess.run([sys.executable, file], stdout=subprocess.PIPE)
    old = subprocess.run([sys.executable, name], stdout=subprocess.PIPE)

    assert new.stdout == old.stdout
