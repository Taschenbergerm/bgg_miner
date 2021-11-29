import dataclasses
import datetime
from typing import Optional, Dict, List

from dataclasses_json import dataclass_json


@dataclass_json
@dataclasses.dataclass
class BoardGameCategory:
    id: int
    name: str


@dataclass_json
@dataclasses.dataclass
class LanguageDependency:
    level: int
    description: str
    votes: int

@dataclass_json
@dataclasses.dataclass
class LanguagePoll:
    total_votes: int
    results: Dict[int, LanguageDependency]



@dataclass_json
@dataclasses.dataclass
class PlayerRecommendation:
    players: str
    best: int
    recommended: int
    not_recommmended: int
    total: Optional[int] = 0

    def __post_init__(self):
        self.total = self.best + self.recommended + self.not_recommmended


@dataclass_json
@dataclasses.dataclass
class PlayerRecommendationPoll:
    total_votes: int
    results: Dict[str, PlayerRecommendation]


@dataclass_json
@dataclasses.dataclass
class BoardGame:
    id: int
    name: str
    description: str
    category: List[str]
    mechanic: List[str]
    image: str = ""
    publication_year: datetime.date.year = None
    player_poll: Dict[str, PlayerRecommendation] = None
    language_poll: Dict[int, int ] = None
    min_player: Optional[int] = None
    max_player: Optional[int] = None
    year: Optional[int] = None
    playtime_max: Optional[int] = None
    rating: Optional[float] = None
    complexity: Optional[float] = None

    def __post_init__(self):
        self.player_poll = self.player_poll or {}
        self.language_poll = self.language_poll or {}


@dataclass_json
@dataclasses.dataclass
class Reference:
    id: int
    name: str


@dataclass_json
@dataclasses.dataclass
class EmptyGame(BoardGame):

    id: int = 0
    name: str = ""
    image: str = ""
    description: str = ""
    category: List[str] = None
    mechanic: List[str] = None

    def __post_init__(self):
        self.category = self.category or []
        self.mechanic = self.mechanic or []

    def __bool__(self):
        return False


class Polls:
    n_players = "suggested_numplayers"
    age = "suggested_playerage"
    language = "language_dependence"


class Tags:
    name = "name"
    image = "image"
    description = "description"
    year = "yearpublished"
    player_may = "minplayers"
    player_min = "maxplayers"
    poll = "poll"
    playtime_avg = "playingtime"
    playtime_max = "maxplaytime"
    playtime_min = "minplaytime"
    link = "link"
    item = "item"
    statistics = "statistics"


class Links:
    mechanic = "boardgamemechanic"
    category = "boardgamecategory"
    family = "boardgamefamily"
    designer = "boardgamedesigner"
    artist = "boardgameartist"
    publisher = "boardgamepublisher"


class StatisticTags:
    statistics = "statistics"
    ratings = "ratings"
    usersrated = "usersrated"
    average = "average"
    bayesaverage = "bayesaverage"
    ranks = "ranks"
    rank = "rank"
    rank = "rank"
    stddev = "stddev"
    median = "median"
    owned = "owned"
    trading = "trading"
    wanting = "wanting"
    wishing = "wishing"
    numcomments = "numcomments"
    numweights = "numweights"
    averageweight = "averageweight"
