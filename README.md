# `ai_forum_qa_bot`

`ai_forum_qa_bot` is a Python package that allows question-answer interaction with the entire corpus of Alignment Forum posts. 


## Developer Quickstart

First thing to do is to create a virtual environment. Install `virtualenv` using
```
pip install virtualenv
```
Then create a virtual environment with
```
python -m virtualenv venv
```
This creates a virtual environment called "venv". Activate it via
```
source venv/bin/activate
```
Great! Now you're ready to install the package.

Install the development version of the package in editable mode to the environment with
```
pip install -e '.[develop]'
```
The package's configuration is in `pyproject.toml` (summary [here](https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html)). If you need a dependency, add it to this file.

Test the package install by opening Python and running `import ai_forum_qa_bot`.

The precommit hooks provide linting and autoformatting. Install them by running
```
pre-commit install
```
These will run automatically each time you commit.
