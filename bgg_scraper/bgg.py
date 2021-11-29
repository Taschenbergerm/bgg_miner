import dataclasses

from loguru import logger
import requests

ROOT_PATH = "https://www.boardgamegeek.com/xmlapi2/"


@dataclasses.dataclass
class Thing:
    name: str
    id: int
    type: str




def get_thing(id: int):

    url = f"{ROOT_PATH}thing?id={id}"
    logger.debug(f"Getting thing from {url}")
    response = requests.get(url)
    if response.status_code != 200:
        logger.error(f"Error getting thing from {url}")
        return None
    xml = response.content
    logger.debug(f"Got thing from {url}")
    return xml