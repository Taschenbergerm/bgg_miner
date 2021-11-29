
from loguru import logger
from lxml import etree

from bgg_scraper import models
from bgg_scraper.models import Tags, Polls, PlayerRecommendationPoll, LanguagePoll, StatisticTags


def parse_into_game(tree: etree):
    game = dict()
    game["category"] = []
    game["mechanic"] = []

    for ele in tree.iter():
        if ele.tag == Tags.item:
            game["id"] = ele.attrib["id"]
        elif ele.tag == Tags.name and ele.attrib.get("type") == "primary":
            game["name"] = ele.attrib["value"]
        elif ele.tag == Tags.image:
            game["image"] = ele.text
        elif ele.tag == Tags.description:
            game["description"] = ele.text
        elif ele.tag == Tags.year:
            game["year"] = ele.attrib["value"]
        elif ele.tag == Tags.playtime_min:
            game["min_player"] = ele.attrib["value"]
        elif ele.tag == Tags.playtime_max:
            game["max_player"] = ele.attrib["value"]
        elif ele.tag == Tags.poll and ele.attrib["name"] == Polls.n_players:
            game["player_poll"] = parse_player_poll(ele)
        elif ele.tag == Tags.poll and ele.attrib["name"] == Polls.language:
            game["language_poll"] = parse_language_poll(ele)
        elif ele.tag == Tags.playtime_avg:
            game["playtime_max"] = ele.attrib["value"]
        elif ele.tag == Tags.playtime_min:
            game["playtime_min"] = ele.attrib["value"]
        elif ele.tag == Tags.playtime_max:
            game["playtime_max"] = ele.attrib["value"]
        elif ele.tag == Tags.link and ele.attrib["type"] == "boardgamecategory":
            game["category"].append(models.Reference(id=ele.attrib["id"], name=ele.attrib["value"]))
        elif ele.tag == Tags.link and ele.attrib["type"] == "boardgamemechanic":
            game["mechanic"].append(models.Reference(id=ele.attrib["id"], name=ele.attrib["value"]))
        elif ele.tag == Tags.statistics:
            statistics = parse_statistics(ele)
        else:
            logger.debug(f"Unparsed tag {ele.tag}")
    boardgame = models.BoardGame(**game, **statistics)
    return boardgame


def parse_statistics(tree: etree):
    statistics = {}
    for e in tree.iter():
        if e.tag == StatisticTags.average:
            statistics["rating"] = e.attrib["value"]
        elif e.tag == StatisticTags.averageweight:
            statistics["complexity"] = e.attrib["value"]
    return statistics


def parse_language_poll(tree: etree):
    total_vote = tree.attrib.get("totalvotes")
    poll_results = {}
    for e in tree.iter():
        if not e.attrib or not e.attrib.get("level"):
            continue
        level = int(e.attrib["level"])
        votes = e.attrib["numvotes"]
        poll_results[level] = models.LanguageDependency(level=level,
                                                        description=e.attrib["value"],
                                                        votes=int(votes))
    return LanguagePoll(total_votes=int(total_vote), results=poll_results)


def parse_player_poll(tree: etree):
    poll_results = {}
    total_vote = tree.attrib.get("totalvotes")
    for e in tree:
        players = e.attrib["numplayers"]
        results = {}
        for result in e:
            value = result.attrib["value"]
            votes = result.attrib["numvotes"]
            results[value] = int(votes)
        poll_results[players] = results
        rec = models.PlayerRecommendation(players,
                                          results.get("Best", 0),
                                          results.get("Recommended", 0),
                                          results.get("Not Recommended", 0)
                                          )
        poll_results[players] = rec
    return PlayerRecommendationPoll(total_vote, poll_results)
