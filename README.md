# `fuzzy-secret-stdout`

> Small utility to fuzzy search from a secret store and print the value to stdout

[![main](https://github.com/kiran94/fuzzy-secret-stdout/actions/workflows/main.yml/badge.svg)](https://github.com/kiran94/fuzzy-secret-stdout/actions/workflows/main.yml)
![GitHub License](https://img.shields.io/github/license/kiran94/fuzzy-secret-stdout)
![PyPI - Version](https://img.shields.io/pypi/v/fuzzy-secret-stdout)

## Install

```bash
python -m pip install fuzzy-secret-stdout
```

Dependencies:

* Python 3.9+
* [`fzf`](https://github.com/junegunn/fzf?tab=readme-ov-file#installation)

## Usage

```bash
# fuzzy search from secrets from aws parameter store
fuzzy-secret-stdout

# alias for the above
fss

# fuzzy search and explicitly specify the secret store to search
fss -i AWS_SSM
```
