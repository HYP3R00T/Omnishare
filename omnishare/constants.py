import os

# Constants
LOG_DIR = os.path.expanduser("~/.omnishare/logs")
CONFIG_DIR = os.path.expanduser("~/.omnishare")
KEY_FILE = os.path.join(CONFIG_DIR, "key.key")
TOKEN_FILE = os.path.join(CONFIG_DIR, "token.json")
CONFIG_FILE = os.path.join(CONFIG_DIR, ".omnisharerc")

CONFIG_DEFAULT_DATA: dict = {
    "linkedin": {"post": True},
    "mastodon": {"post": True},
}

# Endpoints
LINKEDIN_ME_ENDPOINT: str = "https://api.linkedin.com/v2/userinfo"
LINKEDIN_POST_ENDPOINT: str = "https://api.linkedin.com/v2/ugcPosts"
MASTODON_POST_ENDPOINT: str = "https://mastodon.social/api/v1/statuses"
