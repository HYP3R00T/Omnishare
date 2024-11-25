import requests

from omnishare.config import read_config, write_config
from omnishare.constants import LINKEDIN_ME_ENDPOINT, LINKEDIN_POST_ENDPOINT
from omnishare.logger import log_api_call, setup_logger
from omnishare.token_handler import get_token


@log_api_call
def linkedin_post(post) -> requests.Response:
    logger = setup_logger()

    ACCESS_TOKEN = get_token("LinkedIn")
    logger.debug("Got LinkedIn access token from local file")

    config_data = read_config()
    if not config_data.get("linkedin_sub"):
        logger.info("Fetching LinkedIn user ID")
        headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
        response = requests.get(url=LINKEDIN_ME_ENDPOINT, headers=headers)
        person_id = response.json()["sub"]
        config_data["linkedin_sub"] = person_id
        write_config(config_data)
        logger.info("Saved LinkedIn user ID")

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
    }

    json_data = {
        "author": f"urn:li:person:{config_data.get('linkedin_sub')}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": f"{post}"},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }

    logger.info("Posting content")
    response = requests.post(url=LINKEDIN_POST_ENDPOINT, json=json_data, headers=headers)

    if response.status_code == 201:
        logger.info(f"Status code: {response.status_code}")
        logger.info("Sucessfully posted.")
    else:
        logger.error(f"Status code: {response.status_code}")
        logger.error(f"Response: {response}")
    return response
