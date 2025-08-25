from faker import Faker
from typing import List, Dict, Any
from src.models.api_models import (
    SearchRequest, ReleaseChangeRequest, Artist, Venue, Track,
    ShowImage, ReleaseStatus, ObjectType, CatalogType
)
from datetime import datetime

fake = Faker()


class TestDataFactory:
    """Factory for generating test data"""
    
    @staticmethod
    def create_search_request(
        search_string: str = None,
        catalog_ids: List[str] = None,
        user_id: str = None
    ) -> SearchRequest:
        return SearchRequest(
            searchString=search_string or fake.word(),
            catalogIds=catalog_ids or [CatalogType.NUGS],
            userId=user_id or fake.uuid4()
        )
    
    @staticmethod
    def create_artist(artist_id: str = None, name: str = None) -> Artist:
        return Artist(
            id=artist_id or str(fake.random_int(1, 9999)),
            name=name or fake.name(),
            abbreviation=fake.lexify(text="???", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        )
    
    @staticmethod
    def create_venue(venue_id: str = None) -> Venue:
        return Venue(
            id=venue_id or str(fake.random_int(1, 9999)),
            title=fake.company(),
            name=fake.company(),
            city=fake.city(),
            state=fake.state_abbr(),
            country="US"
        )
    
    @staticmethod
    def create_track(track_id: int = None, show_id: int = None) -> Track:
        return Track(
            id=track_id or fake.random_int(1, 9999),
            songTitle=fake.sentence(nb_words=2),
            codecId=fake.random_int(1, 3),
            duration=fake.random_int(120, 600),
            showId=show_id or fake.random_int(1, 9999)
        )
    
    @staticmethod
    def create_release_change_request(
        release_id: int = None,
        status: ReleaseStatus = ReleaseStatus.LIVE,
        catalog_ids: List[CatalogType] = None,
        object_type: ObjectType = ObjectType.SHOW
    ) -> ReleaseChangeRequest:
        artist = TestDataFactory.create_artist()
        venue = TestDataFactory.create_venue()
        tracks = [TestDataFactory.create_track() for _ in range(fake.random_int(1, 5))]
        
        return ReleaseChangeRequest(
            id=release_id or fake.random_int(1, 9999),
            status=status,
            title=fake.sentence(nb_words=3),
            type=object_type,
            catalogIds=catalog_ids or [CatalogType.NUGS],
            showImage=ShowImage(
                showId=fake.random_int(1, 9999),
                url=fake.image_url()
            ),
            artist=artist,
            venue=venue,
            releaseDate=fake.date_time(),
            audioFormats=["mp3", "flac"],
            tracks=tracks
        )

    @staticmethod
    def create_catalog_scenarios() -> Dict[str, List[CatalogType]]:
        """Create different catalog ID scenarios for testing"""
        return {
            "nugs_only": [CatalogType.NUGS],
            "playdead_only": [CatalogType.PLAY_DEAD],
            "both_catalogs": [CatalogType.NUGS, CatalogType.PLAY_DEAD]
        }