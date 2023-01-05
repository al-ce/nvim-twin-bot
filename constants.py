import pytz
import re
from dotenv import dotenv_values

DAY = 86399
UTC = pytz.utc

SUBMISSIONS_LOG = "submissions.json"

TWIN_REPO = "https://github.com/phaazon/this-week-in-neovim-contents/"
BRANCH_URL_BASE = f"{TWIN_REPO}tree/"

ACCESS_TOKEN = dotenv_values(".env")["GH_ACCESS_TOKEN"]
EXCLUDED_FILES = ["HEADER", "example", "did-you-know", "want-to-contribute"]
GIT_REPO_DOMAINS = ["github", "gitlab", "bitbucket", "codeberg"]
REPO_EXP = re.compile(
    r"(https?://(" + "|".join(GIT_REPO_DOMAINS) +
    ")\.com/)([\w-]+)/([\w-]+(\.\w+)?)"
)

BOT_CALLS = [
    "!twinbot-core",
    "!twinbot-help",
    "!twinbot-guides",
    "!twinbot-new",
    "!twinbot-updates",
    "!twinbot",
]

# a regex that can match any item in KW
BOT_CALL_EXP = re.compile(r"(" + "|".join(BOT_CALLS) + r")")

TEMPLATE_LINKS = {
    "core": "https://github.com/phaazon/this-week-in-neovim-contents/blob/master/template/0-core-updates/1-example.md",
    "help": "https://github.com/phaazon/this-week-in-neovim-contents/blob/master/template/1-need-help/1-example.md",
    "guides": "https://github.com/phaazon/this-week-in-neovim-contents/blob/master/template/2-guides/1-example.md",
    "new": "https://github.com/phaazon/this-week-in-neovim-contents/blob/master/template/3-new-plugins/1-example.md",
    "updates": "https://github.com/phaazon/this-week-in-neovim-contents/blob/master/template/4-updates/1-example.md",
}
