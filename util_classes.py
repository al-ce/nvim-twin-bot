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
    """Handle date/time related functions relevant to TWiN repo."""

    def __init__(self):
        self.latest_branch = datetime.fromtimestamp(
            self.last_sunday() + 604800, UTC).strftime("%Y-%b-%d")

    def last_sunday(self) -> datetime:
        """Returns the last Sunday in UTC"""
        ep = time.time()
        now = datetime.fromtimestamp(ep, UTC)
        seconds_elapsed_today = (now.hour * 3600) + \
            (now.minute * 60) + now.second
        weekday = now.weekday()

        return ep - (weekday) * 86400 - seconds_elapsed_today

    def parse_date(self) -> tuple:
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
    """Handles reading and writing to the submissions log"""

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
        self.json_log({}, "w")
        return {}

    def json_log(self, submissions: dict, mode="w"):
        """Log the matched submissions to a json file."""

        with open(self.submissions_path, mode) as f:
            json.dump(submissions, f, indent=4)


class Message:
    """Returns the appropriate message for the bot call."""

    def thank_you(author, repo_url, pr_url):
        """Since we found that the newsworthy repo already has a PR in the
        lastest branch, we thank the PR author for their contribution."""

        return f"""- [How to Contribute to TWiN]({TWIN_REPO}blob/master/README.md#how-to-contribute)\n\n
A [PR]({pr_url}) for this news in the latest TWiN repo may already exist. If we made a mistake (let us know!), please read the guidelines and consider making a pull request.\n\n
Thank you for your contribution to [This Week in Neovim](https://this-week-in-neovim.org)!\n\n
- Automate your TWiN PRs with [@roobert](https://github.com/roobert)'s [twin-sh](https://github.com/roobert/twin-sh) wizard
"""

    def links(author, latest_branch_url, template_link, category):
        """Since we haven't found a PR for the newsworthy repo, we post the
        links to the TWiN guidelines and a link to the PR template."""

        branch_link = f"""- [Latest TWiN branch]({latest_branch_url})
- [Template Directory]({latest_branch_url}/template)""" \
        if latest_branch_url else """- The bot couldn't find next week's branch. Contribute to this Monday's if it's not too late, or consider [creating next week's](https://github.com/phaazon/this-week-in-neovim-contents/fork)!"""

        msg = f"""Hi /u/{author}, please consider making a PR for this news in the upcoming [This Week in Neovim](https://this-week-in-neovim.org/) edition!
- [How to Contribute to TWiN]({TWIN_REPO}blob/master/README.md#how-to-contribute)
{branch_link}
- Streamline your TWiN PRs with the [twin-sh wizard](https://github.com/roobert/twin-sh) by [@roobert](https://github.com/roobert)!
"""

        if latest_branch_url and category != "!twinbot":
            msg += f"""\n\nHere is a [link]({latest_branch_url+template_link}) to a PR template for the `{category}` category.
\n\nPlease read the submission guidelines and check the category before submitting. Thank you!"""

        return msg
