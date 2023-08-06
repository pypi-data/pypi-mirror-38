# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['kuro']
install_requires = \
['black==18.9b0', 'click>=7.0.0,<8.0.0']

entry_points = \
{'console_scripts': ['kuro = kuro:main']}

setup_kwargs = {
    'name': 'kuro',
    'version': '0.0.3',
    'description': 'Run Black (Python code formatter) only on Git unstaged/untracked files',
    'long_description': "# Kuro\n\nRun [Black](https://github.com/ambv/black) (Python code formatter) only on Git unstaged/untracked files\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n## Requirements\n\n* Python 3.6 (f-strings!)\n* [Click](https://github.com/pallets/click)\n* [Black](https://github.com/ambv/black)\n\n## Usage\n\n```\nUsage: kuro [OPTIONS]\n\nOptions:\n  --diff             Create a diff of the changes, in a 'kuro.diff' file. If\n                     you approve the changes, run kuro with --apply_diff.\n  --apply_diff       Consume (and delete) an existing 'kuro.diff' file.\n  --project_options  Setup options for Kuro/Black on a directory level.\n  --help             Show this message and exit.\n\n```\n\nIf you so desire, you can set a different Kuro/Black configuration on a global level by exporting an environment variable called `KURO_BLACK_OPTIONS`.\n\nKuro will prioritize using project options over using global options.\n\nIf no global or local options are set, Kuro will just run Black normally.\n\n## TODO List\n\n* Validation of Black settings saved on `.kuro_config` file\n* Fix applying patch file (slightly broken at the moment)\n",
    'author': 'André Madeira Cortes',
    'author_email': 'amadeiracortes@gmail.com',
    'url': 'https://github.com/BamBalaam/kuro',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
