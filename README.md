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
* Valid [AWS Credentials](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html) available your terminal context

## Usage

```bash
# fuzzy search from secrets from aws parameter store
fuzzy-secret-stdout

# alias for the above
fss

# fuzzy search and explicitly specify the secret store to search
fss -i AWS_SECRET_MAN

# fuzzy search aws secret manager and pipe into jq
fss -i AWS_SECRET_MAN | jq .
```

## Integrations

`fuzzy-secret-stdout` supports the following secret stores:

| Secret Store                                                                                                                             | Command Line Argument  |
| -------------                                                                                                                            | ---------------------- |
| [AWS Systems Manager Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html) | `AWS_SSM`              |
| [AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)                                            | `AWS_SECRET_MAN`       |

The *Command Line Argument* above is passed as the `-i` flag. `AWS_SSM` is the default.
