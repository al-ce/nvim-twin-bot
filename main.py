import praw
from constants import BRANCH_URL_BASE
from util_classes import DateHandler, Message
from util_funcs import (
    check_latest_branch,
    new_repos_in_prs,
    read_new_submissions,
    template_link,
)


REDDIT = praw.Reddit(
    "NvimTWiNBot",
    user_agent="<NvimTWiNBot:1.0 (by u/Thrashymakhus)>",
)


def main():
    date_handler = DateHandler()
    latest_branch = date_handler.latest_branch
    latest_branch_url = f"{BRANCH_URL_BASE}{latest_branch}"
    check_latest_branch(latest_branch_url)
    year, month, day = date_handler.parse_latest_branch()
    current_contents_path = f"contents/{year}/{month}/{day}"

    curr_prs: dict = new_repos_in_prs(current_contents_path)

    subreddit = REDDIT.subreddit("nvimtwindemo")

    past_comments = []

    submissions = read_new_submissions(subreddit, past_comments, 50)

    for k, v in submissions.items():
        for comment_id, bot_call in v["comments"].items():
            past_comments.append(comment_id)
            if bot_call:
                if v["repo"] in curr_prs:
                    msg = Message.thank_you(
                        v["author"],
                        v["repo"],
                        curr_prs[v["repo"]]
                    )
                    print(msg)
                else:
                    category = bot_call.split("-")[-1]
                    link = template_link(category)
                    msg = Message.links(latest_branch, category, link)
                    print(msg)


if __name__ == "__main__":
    main()
