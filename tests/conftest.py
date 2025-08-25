import pytest
from src.api_client.music_api_client import MusicAPIClient
from fixtures.test_data_factory import TestDataFactory
from utils.test_helpers import APITestHelpers


@pytest.fixture(scope="session")
def api_client():
    """Create API client for testing"""
    return MusicAPIClient()


@pytest.fixture(scope="session")
def test_data_factory():
    """Create test data factory"""
    return TestDataFactory()


@pytest.fixture(scope="session")
def test_helpers():
    """Create test helpers"""
    return APITestHelpers()


@pytest.fixture
def sample_search_requests(test_data_factory):
    """Generate sample search requests"""
    return {
        "basic": test_data_factory.create_search_request("Dead and Company"),
        "with_user": test_data_factory.create_search_request("Truckin", user_id="test_user_123"),
        "nugs_only": test_data_factory.create_search_request("Sugar Magnolia", ["nugs"]),
        "playdead_only": test_data_factory.create_search_request("Ripple", ["playDead"]),
        "both_catalogs": test_data_factory.create_search_request("Fire", ["nugs", "playDead"])
    }


@pytest.fixture
def sample_release_changes(test_data_factory):
    """Generate sample release change requests"""
    from src.models.api_models import ReleaseStatus, ObjectType, CatalogType
    
    return {
        "active_show": test_data_factory.create_release_change_request(
            status=ReleaseStatus.LIVE,
            object_type=ObjectType.SHOW
        ),
        "inactive_show": test_data_factory.create_release_change_request(
            status=ReleaseStatus.INACTIVE,
            object_type=ObjectType.SHOW
        ),
        "album_preorder": test_data_factory.create_release_change_request(
            status=ReleaseStatus.PRE_ORDER,
            object_type=ObjectType.ALBUM
        ),
        "cross_catalog": test_data_factory.create_release_change_request(
            catalog_ids=[CatalogType.NUGS, CatalogType.PLAY_DEAD]
        )
    }