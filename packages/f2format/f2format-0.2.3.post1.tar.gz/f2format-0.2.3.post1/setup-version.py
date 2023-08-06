# -*- coding: utf-8 -*-

import os
import re

with open('./f2format.py', 'r') as file:
    for line in file:
        match = re.match(r'^f2format (.*)', line)
        if match is None:
            continue
        __version__ = match.groups()[0]
        break

context = list()
with open(os.path.join(os.path.dirname(__file__), 'setup.py')) as file:
    for line in file:
        match = re.match(r"__version__ = '(.*)'", line)
        if match is None:
            context.append(line)
        else:
            context.append(f'__version__ = {__version__!r}\n')

with open(os.path.join(os.path.dirname(__file__), 'setup.py'), 'w') as file:
    file.writelines(context)

context = list()
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as file:
    for line in file:
        match = re.match(r"^f2format .*", line)
        if match is None:
            context.append(line)
        else:
            context.append(f'f2format {__version__}\n')

with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'w') as file:
    file.writelines(context)
