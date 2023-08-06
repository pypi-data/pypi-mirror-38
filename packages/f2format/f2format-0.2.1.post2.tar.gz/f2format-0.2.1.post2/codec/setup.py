# -*- coding: utf-8 -*-

import distutils.log  # pylint: disable=E0401, E1101, E0611
import os

try:
    from setuptools import setup
    from setuptools.command.install import install as _install
except ImportError:
    from distutils.core import setup
    from distutils.command.install import install as _install

# README
with open('./README.md', 'r') as file:
    long_desc = file.read()

# macro
PTH = '''\
import contextlib

with contextlib.suppress(ImportError):
    import f2format_codec
    f2format_codec.register()
'''


class install(_install):

    def initialize_options(self):
        super().initialize_options()
        # # use this prefix to get loaded as early as possible
        # name = 'aaaaa_%s' % self.distribution.metadata.name
        self.extra_path = (self.distribution.metadata.name, PTH)

    def finalize_options(self):
        super().finalize_options()
        install_suffix = os.path.relpath(self.install_lib, self.install_libbase)  # pylint: disable=E0203
        if install_suffix == '.':
            distutils.log.info('skipping install of .pth during easy-install')  # pylint: disable=E1101
        elif install_suffix == self.extra_path[1]:
            self.install_lib = self.install_libbase
            distutils.log.info("will install .pth to '%s.pth'",  # pylint: disable=E1101
                               os.path.join(self.install_lib, self.extra_path[0]))
        else:
            raise AssertionError('unexpected install_suffix',
                                 self.install_lib, self.install_libbase, install_suffix)


setup(
    name='f2format-codec',
    version='0.0.1',
    author='Jarry Shaw',
    author_email='jarryshaw@icloud.com',
    url='https://github.com/JarryShaw/f2format-codec',
    license='MIT License',
    keywords='fstring f2format codec',
    description='Codec registry for f2format',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    python_requires='>=3.3',
    install_requires=['f2format'],
    py_modules=['f2format_codec'],
    package_data={
        '': [
            'LICENSE',
            'README.md',
            'CHANGELOG.md',
        ],
    },
    classifiers=[
        # 'Development Status :: 4 - Beta',
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
    cmdclass={
        'install': install,
    },
)
