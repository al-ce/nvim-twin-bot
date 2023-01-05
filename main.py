import praw
from constants import BOT_CALL_EXP, BRANCH_URL_BASE, REPO_EXP
from util_classes import DateHandler, Logger, Message
from util_funcs import (
    check_latest_branch,
    new_repos_in_prs,
    regex_check,
    reply_dict_values,
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
    past_replies = logger.submissions

    subreddit = REDDIT.subreddit("nvimtwindemo")

    recent_submissions = [
        sub for sub in subreddit.new(limit=500)
        if date_handler.same_week(sub.created_utc)
        and sub.id not in past_replies
    ]

    for submission in recent_submissions:
        sub_id = submission.id
        author = submission.author.name
        for comment in submission.comments:
            bot_call = regex_check(comment.body, BOT_CALL_EXP)
            if not bot_call:
                continue

            repo = regex_check(submission.selftext, REPO_EXP)
            pr_url = curr_prs.get(repo)
            if repo and pr_url:
                msg = Message.thank_you(author, repo, pr_url)
                reply = 'thanks'
            else:
                category = bot_call.split("-")[-1]
                link = template_link(category)
                msg = Message.links(latest_branch, category, link)
                reply = 'links'

            new_reply = {
                sub_id: reply_dict_values(comment.id, reply, pr_url)
            }

            print(msg)

            logger.json_log(past_replies | new_reply)


if __name__ == "__main__":
    main()
