#!/usr/bin/env python3
# coding: utf-8
# pylint:disable=unused-wildcard-import
from doit.action import CmdAction

POETRY_ENV_RUN = "poetry run"
PYTHON_SCRIPT_CMD = "python -m"

def task_rungr():
    return {
        "actions": [CmdAction(f"{POETRY_ENV_RUN} {PYTHON_SCRIPT_CMD} exec_gradio")],
        'verbosity': 2,
    }