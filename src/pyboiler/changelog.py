import datetime as dt
import json
from urllib import error, request


class Commit:
    def __init__(self, data: dict):
        self.sha: str = data["sha"]

        commit: dict = data["commit"]

        self.author: dict = commit["author"]
        self.committer: dict = commit["committer"]
        self.message: str = commit["message"]

        self.url: str = data["html_url"]

        self.strings: list = [
            f"{self.author['date']}: {self.message}",
            f"{self.author['name']}: {self.author['email']}",
            f"{self.committer['name']}: {self.committer['email']}",
            f"{self.url}",
        ]

    def __repr__(self):
        return f"<Commit {self.sha}>"

    def __str__(self) -> str:
        return "\n".join(list(self))

    def __iter__(self):
        for item in self.strings:
            yield item


def Changelog(org: str, repo: str, limit: int = 10) -> dict:
    resp = None
    try:
        resp = request.urlopen(f"https://api.github.com/repos/{org}/{repo}/commits")
    except error.HTTPError:
        return []
    resp = resp.read().decode("UTF-8")
    data = json.loads(resp)

    commits = {"total": len(data), "commits": []}
    for idx, item in enumerate(data):
        if idx == limit:
            break
        commits["commits"].append(Commit(item))
    return commits
