# 🤖 nvim-TWiN-bot
A Reddit bot to help [r/neovim](https://reddit.com/r/neovim) users to contribute to [This Week in Neovim](https://this-week-in-neovim.org) ([Github](https://github.com/phaazon/this-week-in-neovim-contents))

## Why this bot

This bot replies to calls (e.g. `!twinbot`) by a Redditor that sees a post in `r/neovim` they think is newsworthy with links and templates to help make a pull request in the latest TWiN contents branch. The hope is that by seeing how simple the template is and how clear the PR guidelines are, Redditors will be encouraged to help contribute to TWiN rather than leaving it all up to the repo maintainer.

## Usage
Reply to any post in `r/neovim` with any of the following:

    !twinbot-core
    !twinbot-help
    !twinbot-guides
    !twinbot-new
    !twinbot-update
    !twinbot

The bot will respond to any call with helpful links, and if a flag is added to the call (e.g. `-new`), a tag will be added to the message with a link to a specific template.

<img width="500" alt="Bot call with flag" src="https://user-images.githubusercontent.com/23170004/210938563-265ff3fa-0735-4ba5-9da6-59cb47041018.png">

However, if the bot finds a PR in the latest branch of [TWiN](https://github.com/phaazon/this-week-in-neovim-contents) that contains a repo mentioned in the original Reddit submission, the bot will suggest that a TWiN PR may have already been created. We do this to hedge against duplicate PRs and also as a way to say thanks to whoever made the PR (likely the OP).

<img width="500" alt="PR exists" src="https://user-images.githubusercontent.com/23170004/210934620-5fc36fad-bec2-4c2e-bf61-e832fee38fb8.png">

## Structure of the program

Using the [Reddit Python API Wrapper](https://praw.readthedocs.io/en/stable/index.html), we create an instance of `r/neovim` and loop over the comment stream, checking any new commment.
At the top of each loop:
- Instantiate a `DateHandler` object that helps us with all the datetime related functions: given the Unix timestamp of `last_sunday()`, what is the name of the `latest_branch` going to be in format `%Y-%m-%d %H:%M:%S`?
- Instantiate a `Logger` object that reads a `.json` file containing any previous replies by the bot into memory. The `.json` log's role in the execution of the program is to prevent duplicate replies by the bot in the same thread (though it's unlikely that two people would call it the bot in the same thread)
- If the current comment in the stream is `a)` older than last Sunday (UTC), `b)` a child of a post that the bot has already replied to, or `c)` lacking a valid `bot_call`, continues on to the next comment in the stream loop
- Else, get all the `pr_url`s of any PR in the coming week's TWiN branch that contain a link to a repo potentially mentioned in the Reddit post
- If there is no such link, provide all the boilerplate links and a link to a template corresponding to the category flag (if there is one). Since the `DateHandler` object helped determine the link to the current branch, we can make sure the links point to that branch, with the hope the bot is doing its part to help prevent PRs to `main`. 
- Else, reply with a `thank_you` message to the Redditor that called the bot, and mention that a PR for the post they are referencing seems to be open already
- Log the reply and all the relevant data (id of the OP's post, commend id, the type of reply, and a reference number of the PR if one was found) in the `.json` file

## TODO
- Automate deleting any subdirectories in `json/` that are `x` weeks old (probably four?)
- Log some additional useful info (e.g., using inclusive and exclusive keywords, we can log all the Reddit posts from this week that might be good candidates for a PR)
- Write some scripts to help parse the logs for useful information (e.g., filter all the submissions that already have a PR, or vice versa)
