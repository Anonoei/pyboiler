"""Easy to use custom exceptions

Example usage:
```python
from pyboiler.error import Error

class MyCustomError(Error):
    msg = "This is a custom error!"

raise MyCustomError()
raise MyCustomError("Failed because why not")
```
"""


class Error(Exception):
    msg = "None"

    def __init__(self, adtl=None):
        err_msg = self.msg
        if adtl is not None:
            err_msg += f" {adtl}"
        super().__init__(err_msg)


class _Error:
    class InvalidLevel(Exception):
        def __init__(self, level: str):
            super().__init__(
                f"Logging level must be string or Logging.Level - got: '{type(level)}'"
            )
