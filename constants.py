import pytz
import re
from dotenv import dotenv_values

DAY = 86399
UTC = pytz.utc

SUBMISSIONS_LOG = "submissions.json"

TWIN_REPO = 'https://github.com/phaazon/this-week-in-neovim-contents/'
BRANCH_URL_BASE = f"{TWIN_REPO}tree/"

ACCESS_TOKEN = dotenv_values(".env")["GH_ACCESS_TOKEN"]
EXCLUDED_FILES = ["HEADER", "example", "did-you-know", "want-to-contribute"]
GIT_REPO_DOMAINS = ["github", "gitlab", "bitbucket", "codeberg"]
REPO_EXP = re.compile(
    r"(https?://(" + "|".join(GIT_REPO_DOMAINS) +
    ")\.com/)([\w-]+)/([\w-]+(\.\w+)?)"
)

KW = [
    "!twinbot-core",
    "!twinbot-help",
    "!twinbot-guides",
    "!twinbot-new",
    "!twinbot-updates",
    "!twinbot",
]

# a regex that can match any item in KW
KW_EXP = re.compile(r"(" + "|".join(KW) + r")")
