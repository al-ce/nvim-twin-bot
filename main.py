from time import sleep

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
    get_template_link,
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

    for comment in subreddit.stream.comments(skip_existing=True):
        date_handler = DateHandler()
        last_sunday = date_handler.last_sunday()
        latest_branch = date_handler.latest_branch
        logger = Logger(latest_branch)
        past_replies = logger.submissions
        bot_call = regex_check(comment.body, BOT_CALL_EXP)

        print("-" * 20)
        print(f"Submission Title: {comment.submission.title}")
        print(f"Comment ID: {comment.id}")
        print(f"\n{comment.body}\n\n")

        # We might want this condition to keep the logs clean, but it's
        # otherwise too restrictive
        # if comment.created_utc > last_sunday:
        #     print("Not a valid comment: too old")
        #     continue

        if not bot_call:
            print("Not a valid comment: no bot call")
            continue
        if comment.submission.id in past_replies:
            print("Not a valid comment: replied to this submission this week")
            continue

        print("-" * 20)
        print("Beginning reply sequence...")
        print("-" * 20)
        print(f"Last Sunday: {last_sunday}")
        print(f"Latest branch: {latest_branch}")

        sub_id = comment.submission.id
        author = comment.submission.author.name
        category = bot_call.split("-")[-1]
        template_link = get_template_link(category)
        print(f"Category: {category}\nTemplate Link: {template_link}")
        pr_url = None
        latest_branch_url = f"{BRANCH_URL_BASE}{latest_branch}"

        if check_latest_branch(latest_branch_url):
            # If we can't find this week's branch (it's probably late Sunday),
            # we don't run this block.
            year, month, day = date_handler.parse_date()
            current_contents_path = f"contents/{year}/{month}/{day}"
            curr_prs: dict = new_repos_in_prs(current_contents_path)

            repo = regex_check(comment.submission.selftext, REPO_EXP)
            pr_url = curr_prs.get(repo)
        else:
            latest_branch_url = None

        if pr_url:
            # If the repo referenced in OP's submission has a PR, say thx
            msg = Message.thank_you(author, repo, pr_url)
            reply = 'thanks'
        else:

            msg = Message.links(author, latest_branch_url,
                                template_link, category)
            reply = 'links'
            pr_url = None

        print(f"Replying to {sub_id}-{comment.id}...")
        print(msg)
        comment.reply(body=msg)

        logger.json_log(
            past_replies |
            {sub_id: reply_dict_values(comment.id, reply, pr_number(pr_url))}
        )

        # Sleep for 2 mins in case we get too spammy
        sleep_time = 120
        print(f"Bot is sleeping for {sleep_time} seconds...")
        sleep(sleep_time)


if __name__ == "__main__":
    main()
