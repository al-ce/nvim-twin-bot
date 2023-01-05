import praw
from constants import BRANCH_URL_BASE
from util_classes import DateHandler, Logger, Message
from util_funcs import (
    check_latest_branch,
    new_repos_in_prs,
    read_submissions,
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

    # Read past submissions in this week's branch
    logger = Logger(latest_branch)
    past_submissions = logger.submissions

    subreddit = REDDIT.subreddit("nvimtwindemo")

    bot_replies_new = {}

    new_subs = read_submissions(subreddit, past_submissions, 50)


    for sub_id, info in new_subs.items():
        for comment_id, bot_call in info["comments"].items():
            if bot_call:
                if info["repo"] in curr_prs:
                    msg = Message.thank_you(
                        info["author"],
                        info["repo"],
                        curr_prs[info["repo"]]
                    )
                    print(msg)
                    bot_replies_new[sub_id] = {
                            "sub_title": info["title"],
                            "comment_id": comment_id,
                            "message": 'thanks'
                        }

                else:
                    category = bot_call.split("-")[-1]
                    link = template_link(category)
                    msg = Message.links(latest_branch, category, link)
                    print(msg)
                    bot_replies_new[sub_id] = {
                            "sub_title": info["title"],
                            "comment_id": comment_id,
                            "message": 'links'
                        }
            else:
                print(sub_id, info["title"], " | no bot call")



    # Append new submissions to the log
    logger.json_log(past_submissions | bot_replies_new)


if __name__ == "__main__":
    main()
