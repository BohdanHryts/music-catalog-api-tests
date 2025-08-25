from typing import List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class CatalogType(str, Enum):
    NUGS = "nugs"
    PLAY_DEAD = "playDead"


class ReleaseStatus(int, Enum):
    INACTIVE = 0
    LIVE = 1
    PRE_ORDER = 2
    STAGING_ONLY = 4
    HIDDEN_LIVE = 5
    HIDDEN_PRE_ORDER = 7


class ObjectType(str, Enum):
    SHOW = "show"
    ALBUM = "album"


# Search Models
class SearchRequest(BaseModel):
    searchString: str = Field(..., min_length=1)
    catalogIds: List[CatalogType] = Field(default=[CatalogType.NUGS])
    userId: Optional[str] = None


class SearchResultItem(BaseModel):
    id: str
    title: Optional[str] = None
    name: Optional[str] = None


class SearchResponse(BaseModel):
    albums: List[SearchResultItem] = []
    artists: List[SearchResultItem] = []
    tracks: List[SearchResultItem] = []
    venues: List[SearchResultItem] = []
    performanceYears: List[dict] = []
    performanceDates: List[dict] = []


# Release Changes Models
class ShowImage(BaseModel):
    showId: int
    url: str


class ReleaseImage(BaseModel):
    id: str
    name: str
    description: str
    url: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    caption: Optional[str] = None


class Artist(BaseModel):
    id: str
    name: str
    abbreviation: Optional[str] = None


class Venue(BaseModel):
    id: str
    title: Optional[str] = None
    name: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None


class Track(BaseModel):
    id: int
    songTitle: str
    codecId: int
    duration: int
    showId: int


class ReleaseChangeRequest(BaseModel):
    id: int
    status: ReleaseStatus
    title: str
    type: ObjectType
    catalogIds: List[CatalogType] = Field(default=[CatalogType.NUGS])
    showImage: Optional[ShowImage] = None
    releaseImage: Optional[ReleaseImage] = None
    albumTitle: Optional[str] = None
    albumAbbr: Optional[str] = None
    albumReleaseDate: Optional[datetime] = None
    artist: Artist
    venue: Optional[Venue] = None
    releaseDate: datetime
    audioFormats: List[str] = []
    tracks: List[Track] = []