import json
import pathlib
import sys
import time

import requests
from loguru import logger
from jaeger_client import Config
from lxml import etree

from bgg_scraper import exc
from bgg_scraper import parsing
from bgg_scraper import models


def init_tracer(service):
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name=service,
    )

    return config.initialize_tracer()


class BoardGameLoader:

    def __init__(self, chunk_size=1000, offset=0, service_name='boardgame-scaper'):
        self.tracer = init_tracer(service_name)
        self.chunk_size = chunk_size
        self.chunk = 1
        self.offset = offset
        self.last_thing = 0
        self.output_path = pathlib.Path(__file__).parent / "out"
        self.output_path.mkdir(exist_ok=True)
        self.games = []
        self.current_span = None

    def main(self):

        with self.tracer.start_active_span('scrape-loop') as scope:
            while True:
                self.scrape_chunk()

    def scrape_chunk(self):
        with self.tracer.start_active_span(f'scrape-chunk-{self.chunk}') as scope:
            i = 1
            while i < self.chunk_size:
                id = i + self.offset
                try:
                    scope.span.log_kv({'event': "start-scrape", "thing-id": id})
                    game = self.parse_thing(id, 0)
                    if game:
                        self.games.append(game)
                    self.last_thing = id
                except exc.BggNoMoreThingsError as e:
                    logger.warning(f"Propagate Error - {e}")
                    scope.span.log_kv({'event': "finish-scrape", "thing-id": id, "value": "SUCCESS"})
                    self.flush()
                    raise e
                except KeyboardInterrupt as e:
                    logger.warning("Graceful Shutdown")
                    self.flush()
                    sys.exit(0)
                except Exception as e:
                    logger.error(f"Failed to parse {id} due to {e}")
                    scope.span.log_kv({'event': "finish-scrape", "thing-id": id, "value": "ERROR", "error": str(e)})
                    self.flush()
                    raise e
                i += 1
            self.flush()
            self.offset += self.chunk_size
            self.chunk += 1

    def flush(self):
        all_games = [game.to_dict() for game in self.games]
        self.current_span.log_kv({'event': "flush", "chunk": self.chunk, "games": len(all_games)})
        file = self.output_path / f"boardgames_chunk_{self.offset}_{self.last_thing}.json"
        with open(file, "w") as f:
            json.dump(all_games, f, indent=4)
        logger.success(f"Flushed {len(self.games)} games to {file.name}")
        self.games = []

    def parse_thing(self, i: int, retry_counter):
        with self.tracer.start_active_span(f'parse-{i}-{retry_counter}') as scope:
            self.current_span = scope.span
            self.current_span.set_tag('thing-id', i)
            logger.info(f"Try Scraping Thing {i} | Try Counter {retry_counter}")
            url = f"https://www.boardgamegeek.com/xmlapi2/thing"
            response = requests.get(url, params={"id": i, "stats": 1})
            if response.ok:
                game = self.parse_tree(response)
                if game:
                    self.current_span.set_tag('state', 'SUCCESS')
                    logger.success(f"Parsed {game.name}")
                else:
                    game = models.EmptyGame()
            else:
                if retry_counter >= 10:
                    self.current_span.set_tag('state', "ERROR")
                    logger.error(f"Failed to parse {url}")
                    raise exc.BggNoMoreThingsError(f"Failed to parse {url}")
                time.sleep(1 + (2*retry_counter))
                game = self.parse_thing(i, retry_counter + 1)
            game.id = i
            return game

    def parse_tree(self, response: requests.Response):
        entity = etree.fromstring(response.content)
        if not entity:
            self.current_span.set_tag("thing-type", "no-entity")
            return models.EmptyGame()
        entity_type = entity[0].attrib["type"]
        self.current_span.set_tag("thing-type", entity_type)
        if entity_type == "boardgame":
            game = parsing.parse_into_game(entity)
            return game
        else:
            logger.warning(f"Found unknown type - {entity_type} ")
            return models.EmptyGame()

