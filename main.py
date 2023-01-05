import praw
from constants import BOT_CALL_EXP, BRANCH_URL_BASE, REPO_EXP
from util_classes import DateHandler, Logger, Message
from util_funcs import (
    check_latest_branch,
    new_repos_in_prs,
    pr_number,
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
    last_sunday = date_handler.last_sunday()
    latest_branch = date_handler.latest_branch
    latest_branch_url = f"{BRANCH_URL_BASE}{latest_branch}"
    check_latest_branch(latest_branch_url)
    year, month, day = date_handler.parse_date()
    current_contents_path = f"contents/{year}/{month}/{day}"

    curr_prs: dict = new_repos_in_prs(current_contents_path)

    # Read past submissions in this week's branch
    logger = Logger(latest_branch)
    past_replies = logger.submissions

    subreddit = REDDIT.subreddit("nvimtwindemo")

    recent_comments = [
        comment for sub in subreddit.new(limit=500)
        for comment in sub.comments
        if comment.created_utc > last_sunday
        and sub.id not in past_replies
        and regex_check(comment.body, BOT_CALL_EXP)
    ]

    for comment in recent_comments:
        sub_id = comment.submission.id
        author = comment.submission.author.name
        bot_call = regex_check(comment.body, BOT_CALL_EXP)
        repo = regex_check(comment.submission.selftext, REPO_EXP)
        pr_url = curr_prs.get(repo)
        msg = Message.thank_you(author, repo, pr_url)
        reply = 'thanks'

        if not pr_url:
            category = bot_call.split("-")[-1]
            link = template_link(category)
            msg = Message.links(latest_branch, category, link)
            reply = 'links'

        print(msg)

        logger.json_log(
            past_replies |
            {sub_id: reply_dict_values(comment.id, reply, pr_number(pr_url))}
        )


if __name__ == "__main__":
    main()
