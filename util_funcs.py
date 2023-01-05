import urllib.request
from github import Github

from constants import ACCESS_TOKEN, EXCLUDED_FILES, BOT_CALL_EXP, REPO_EXP, TEMPLATE_LINKS


def check_latest_branch(url: str):
    try:
        urllib.request.urlopen(url)
        # Assume that the first matching url is the repo link
        return
    except urllib.error.HTTPError:
        print(f"HTTPError: {urllib.error.HTTPError.code}")
        print("Next week's branch not found. Exiting...")
        quit()


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

    g = Github(ACCESS_TOKEN)
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
    # Return the referenced repo links from the new PRs
    return {
        REPO_EXP.search(new_prs[pr_url][file_patch]).group(0): pr_url
        for pr_url in new_prs
        for file_patch in new_prs[pr_url]
    }


def read_submissions(subreddit, past_submissions: list, limit=50):

    return {
        submission.id: {
            "author": submission.author.name,
            "title": submission.title,
            "comments": {
                comment.id: regex_check(comment.body, BOT_CALL_EXP)
                for comment in submission.comments
                if submission.id not in past_submissions
            },
            # This only grabs the first repo match, so it's possible we might
            # get a false negative, but this is preferable to a false positive
            # when we decide whether to thank the user or post links.
            "repo": regex_check(submission.selftext, REPO_EXP),
        }
        for submission in subreddit.new(limit=50)
    }


def regex_check(body: str, expression: str) -> str:
    regex_match = expression.search(body)
    if regex_match:
        return regex_match.group(0)
    return None


def template_link(bot_call: str) -> str:
    bot_call.split("-")
    return TEMPLATE_LINKS[bot_call]
