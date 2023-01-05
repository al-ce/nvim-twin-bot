from constants import (
    DAY,
    UTC,
    TWIN_REPO,
    SUBMISSIONS_LOG,
)
from datetime import datetime
import json
from pathlib import Path
import time


class DateHandler:

    def __init__(self):
        self.latest_branch = datetime.fromtimestamp(
            self.get_last_sunday() + 604800, UTC).strftime("%Y-%b-%d")

    def get_last_sunday(self) -> datetime:

        ep = time.time()
        now = datetime.fromtimestamp(ep, UTC)
        seconds_elapsed_today = (now.hour * 3600) + \
            (now.minute * 60) + now.second
        weekday = now.weekday()

        return ep - (weekday) * 86400 - seconds_elapsed_today

    def parse_latest_branch(self) -> tuple:
        date = self.latest_branch.split("-")
        return date[0], date[1], date[2]

    def current_time(self) -> datetime:
        """Returns current time in UTC in format: 2020-01-01 00:00:00"""
        return datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")

    def day_passed(self, unix_time: str) -> bool:
        """Returns True if a day has passed since unix_time"""
        time_passed = time.time() - int(unix_time)
        if time_passed > DAY:
            return True
        return False


class Logger:
    """Log the submissions to a json file."""

    def __init__(self, latest_branch: str):
        self.branch = latest_branch
        self.submissions_path = Path(
            f"json/{self.branch}/{SUBMISSIONS_LOG}").resolve()
        self.submissions = self.read(self.submissions_path)

    def read(self, path: Path) -> dict:
        """Get the submissions from a json file."""
        if path.exists():
            with open(path, "r") as f:
                return json.load(f)

        Path(f"json/{self.branch}").mkdir(parents=True, exist_ok=True)
        return {}

    def json_log(self, submissions: dict, mode="a"):
        """Log the matched submissions to a json file."""

        with open(self.submissions_path, mode) as f:
            json.dump(submissions, f, indent=4)


class Message:

    def thank_you(author: str, repo_url: str, pr_url: str) -> str:
        """Since we found that the newsworthy repo already has a PR in the
        lastest branch, we thank the PR author for their contribution."""

        return f"""Hey /u/{author}! It looks like you or someone on your behalf has already submitted a PR for this post to the upcoming TWiN edition!
Repo: {repo_url}
PR url: {pr_url}
Thank you for your contribution to This Week in Neovim!"""

    def links(lastest_branch: str, template: str) -> str:
        """Since we haven't found a PR for the newsworthy repo, we post the
        links to the TWiN guidelines and a link to the PR template."""

        return f"""Someone thinks this post is newsworthy, but the TWiNBot didn't find a PR for it for the latest This Week in Neovim. Consider making a PR! Here are some links to help you out:
- TWiN main page: https://this-week-in-neovim.org/
- How to Contribute to TWiN: {TWIN_REPO}blob/master/README.md#how-to-contribute
- Latest TWiN contents repo branch: {TWIN_REPO}tree/{lastest_branch}
We've also pregenerated a PR template for you, but please make sure to read the guidelines first!
(in particular, please check that the id values in the template match the folder you are submitting to)
```
{template}
````"""
