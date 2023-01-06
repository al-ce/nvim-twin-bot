import praw
from constants import (
    BOT_CALL_EXP,
    BRANCH_URL_BASE,
    REDDIT_ID,
    REDDIT_PASSWORD,
    REDDIT_SECRET,
    REPO_EXP
)
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
    user_agent="<NvimTWiNBot:1.0 (by u/Thrashymakhus)>",
    username="NvimTWiNBot",
    password=REDDIT_PASSWORD,
    client_id=REDDIT_ID,
    client_secret=REDDIT_SECRET,
)


def main():

    subreddit = REDDIT.subreddit("nvimtwindemo")

    for comment in subreddit.stream.comments(skip_existing=False):
        date_handler = DateHandler()
        last_sunday = date_handler.last_sunday()
        latest_branch = date_handler.latest_branch
        logger = Logger(latest_branch)
        past_replies = logger.submissions
        bot_call = regex_check(comment.body, BOT_CALL_EXP)

        # print("-" * 20)
        # print(f"Submission Title: {comment.submission.title}")
        # print(f"Comment ID: {comment.id}")
        # print(f"\n{comment.body}\n\n")

        if (
            comment.created_utc > last_sunday
            or comment.submission.id not in past_replies
            or not bot_call
        ):
            # print("Not a valid comment")
            continue

        latest_branch_url = f"{BRANCH_URL_BASE}{latest_branch}"
        check_latest_branch(latest_branch_url)
        year, month, day = date_handler.parse_date()
        current_contents_path = f"contents/{year}/{month}/{day}"
        curr_prs: dict = new_repos_in_prs(current_contents_path)

        sub_id = comment.submission.id
        author = comment.submission.author.name
        repo = regex_check(comment.submission.selftext, REPO_EXP)
        pr_url = curr_prs.get(repo)
        msg = Message.thank_you(author, repo, pr_url)
        reply = 'thanks'

        if not pr_url:
            category = bot_call.split("-")[-1]
            link = template_link(category)
            msg = Message.links(author, latest_branch, link, category)
            reply = 'links'

        # print(f"Replying to {sub_id}-{comment.id}")
        # print(msg)
        comment.reply(body=msg)

        logger.json_log(
            past_replies |
            {sub_id: reply_dict_values(comment.id, reply, pr_number(pr_url))}
        )


if __name__ == "__main__":
    main()
