import urllib.request
from github import Github

from constants import (
    GH_TOKEN,
    EXCLUDED_FILES,
    REPO_EXP,
    TEMPLATE_LINKS,
)
from util_classes import DateHandler


def check_latest_branch(url: str):
    """Check that the latest branch has been created."""
    print(f"Checking branch url: \n\t{url}")
    try:
        urllib.request.urlopen(url)
        # Assume that the first matching url is the repo link
        return True
    except urllib.error.HTTPError:
        print(f"HTTPError: {urllib.error.HTTPError}")
        print("This week's branch not found.")
        return False


def check_url_status(repo_links: list):
    """Return the first link that returns a 200 status code."""
    for repo_url in repo_links:
        try:
            urllib.request.urlopen(repo_url)
            # Assume that the first matching url is the repo link
            return repo_url
        except urllib.error.HTTPError:
            print(f"HTTPError: {urllib.error.HTTPError.code}")
    return None


def new_repos_in_prs(current_contents_path: str) -> dict:
    """Returns a dict of mentioned repos in this week's PRs."""

    g = Github(GH_TOKEN)
    repo = g.get_repo("phaazon/this-week-in-neovim-contents")
    prs = repo.get_pulls(state="open")

    new_prs = {
        pr.html_url: {
            file.filename: file.patch
            for file in pr.get_files()
            if not any(x in file.filename for x in EXCLUDED_FILES)
            and current_contents_path in file.filename
        }
        for pr in prs
    }

    [print(f"{k}:\n\t{v}") for k, v in new_prs.items()]

    # Return the referenced repo links from the new PRs
    return {
        REPO_EXP.search(new_prs[pr_url][file_patch]).group(0): pr_url
        for pr_url in new_prs
        for file_patch in new_prs[pr_url]
        if REPO_EXP.search(new_prs[pr_url][file_patch])
    }


def pr_number(pr_url: str) -> str:
    """Return the PR number from the PR url."""
    if not pr_url:
        return None
    return pr_url.split("/")[-1]


def regex_check(body: str, expression: str) -> str:
    """Return the first match from the regex expression if it matches."""
    regex_match = expression.search(body)
    if regex_match:
        return regex_match.group(0)
    return None


def reply_dict_values(comment_id, msg, pr_url) -> dict:
    """Set the default values for the new entry in the reply dict."""
    return {
        "call_comment_id": comment_id,
        "message": msg,
        "pr": pr_url,
        "reply_time": DateHandler().current_time(),
    }


def get_template_link(category: str) -> str:
    """Return the relevant template link for the bot call."""
    return TEMPLATE_LINKS.get(category)
