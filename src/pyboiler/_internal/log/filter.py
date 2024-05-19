"""Wrap python.logging filters"""


class Filter:
    """Wrap python.logging.Filter"""

    def __init__(self):
        self.filters = []

    def add_filter(self, filter):
        """Add the specified filter to this handler."""
        if not filter in self.filters:
            self.filters.append(filter)

    def rm_filter(self, filter):
        """Remove the specified filter from this handler."""
        if filter in self.filters:
            self.filters.remove(filter)
