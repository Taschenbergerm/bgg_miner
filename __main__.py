import sys

from loguru import logger

from bgg_scraper.scraper import BoardGameLoader


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stdout, level="INFO")

    bgg_loader = BoardGameLoader(chunk_size=1000, offset=174249)
    bgg_loader.main()
    logger.success("Done")
