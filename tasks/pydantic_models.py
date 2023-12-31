from pydantic import BaseModel
from typing import List, Optional


class MTGTop8Data(BaseModel):

    name: str
    endpoint: str
    percentage: str
    decks: List


class MTGTop8DataDeck(BaseModel):

    author: str
    event: str
    level: int
    rank: int
    date: str
    link: str
    cards: List[dict[str, str]]


class MTGData(BaseModel):

    name: str
    released_at: str
    uri: str
    mana_cost: str
    type_line: str
    oracle_text: str
    colors: List[str] | float
    keywords: List[str]
    set_id: str
    set_name: str
    set_uri: str
    rarity: str
    flavor_text: str
    artist: str
    prices: dict[str, Optional[str], Optional[str],
                 str, Optional[str], Optional[str]]
    power: Optional[str]
    toughness: Optional[str]
