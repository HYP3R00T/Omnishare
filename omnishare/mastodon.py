import requests

from omnishare.constants import MASTODON_POST_ENDPOINT
from omnishare.logger import log_api_call, setup_logger
from omnishare.token_handler import get_token


@log_api_call
def mastodon_post(post) -> requests.Response:
    logger = setup_logger()

    ACCESS_TOKEN = get_token("Mastodon")
    logger.debug("Got Mastodon access token from local file")

    header = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    json_data = {"status": f"{post}"}

    logger.info("Posting content")
    response = requests.post(url=MASTODON_POST_ENDPOINT, data=json_data, headers=header)

    if response.status_code == 200:
        logger.info(f"Status code: {response.status_code}")
        logger.info("Sucessfully posted.")
    else:
        logger.error(f"Status code: {response.status_code}")
        logger.error(f"Response: {response}")
    return response
