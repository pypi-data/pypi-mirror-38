
class Patch(object):
    def __init__(self, jira_issue, logger=None, description=""):
        self._log = logger
        self.jira_issue = jira_issue
        self.description = description

    def __enter__(self):
        pass

    def __exit__(self):
        pass

    def __call__(self, fun):
        def _inner(*args, **kwargs):
            return fun(*args, **kwargs)

        return _inner




