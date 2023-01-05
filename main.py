import praw
from constants import BOT_CALL_EXP, BRANCH_URL_BASE, REPO_EXP
from util_classes import DateHandler, Logger, Message
from util_funcs import (
    check_latest_branch,
    new_repos_in_prs,
    regex_check,
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

    recent_submissions = [sub for sub in subreddit.new(
        limit=500) if date_handler.same_week(sub.created_utc)]

    for submission in recent_submissions:
        if submission.id in past_submissions:
            continue
        author = submission.author.name
        submission_id = submission.id
        for comment in submission.comments:
            bot_call = regex_check(comment.body, BOT_CALL_EXP)
            if not bot_call:
                continue

            bot_replies_new[submission_id] = {
                "author": author,
                "title": submission.title,
                "url": submission.url,
                "comment_id": comment.id,
                "message": 'links',
            }

            repo = regex_check(submission.selftext, REPO_EXP)
            if repo and repo in curr_prs:
                pr_url = curr_prs[repo]
                msg = Message.thank_you(author, repo, pr_url)
                print(msg)
                bot_replies_new[submission_id]["message"] = 'thanks'
                bot_replies_new[submission_id]["pr_url"] = pr_url
            else:
                category = bot_call.split("-")[-1]
                link = template_link(category)
                msg = Message.links(latest_branch, category, link)
                print(msg)

            logger.json_log(past_submissions | bot_replies_new)

if __name__ == "__main__":
    main()
