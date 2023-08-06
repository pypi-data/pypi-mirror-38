# GitHub Cards

[![PyPI](https://img.shields.io/pypi/v/github_cards.svg)](https://pypi.python.org/pypi/github_cards)
[![Travis](https://img.shields.io/travis/larsrinn/github_cards.svg)](https://travis-ci.org/larsrinn/github_cards)
[![Documentation Status](https://readthedocs.org/projects/github-cards/badge/?version=latest)](https://github-cards.readthedocs.io/en/latest/?badge=latest)

Convert your GitHub issues into printable cards for your physical Scrum board.

* Free software: MIT license
* Documentation: https://github-cards.readthedocs.io.


## Features

This tool creates a printable HTML-file containing the issues of a GitHub repository.
You can print the file, cut the cards and attach them to your physical Scrum/Kanban board.

To use it, run

```bash
# github_cards REPOSITORY_OWNER REPOSITORY_NAME
github_cards pallets click
```

There are some options available, e.g. to access private repositories or only select a certain milestone.

```bash
github_cards --help

# Usage: github_cards [OPTIONS] OWNER REPOSITORY
#
# Console script for github_cards.
#
# Options:
#  -u, --username TEXT
#  -m, --milestone-title TEXT
#  -m#, --milestone-number TEXT
#  -s, --state TEXT
#  -o, --output TEXT
#  --help                        Show this message and exit.

```

### ToDo
* [ ] Unspaghettify
* [ ] Add some tests
* [ ] Add documentation
* [ ] Caching of already covered cards

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.
