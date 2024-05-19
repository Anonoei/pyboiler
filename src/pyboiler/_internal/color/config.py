import re

from ...generic import storage

__init = False

if not __init:
    __init = True
    config = storage()
    config.TAG_START = "<c"
    config.TAG_END = ">"
    config.TAG_RE = re.compile(
        config.TAG_START + r"\w+" + config.TAG_END, re.IGNORECASE
    )
