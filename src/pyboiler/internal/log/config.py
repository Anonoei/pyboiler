import re

from ...generic import storage

__init = False

if not __init:
    __init = True
    config = storage()
    config.SENTINEL = object()
    config.DFLT_FMT = "<#time> <<#name>> <#levelname>: <#message>"
    config.DFLT_DATEFMT = "%Y-%m-%d_%H.%M.%S"
    config.TAG_START = "<#"
    config.TAG_END = ">"
    config.TAG_RE = re.compile(
        config.TAG_START + r"\w+" + config.TAG_END, re.IGNORECASE
    )
