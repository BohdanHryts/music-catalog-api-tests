from typing import Dict, Any, List
from src.api_client.base_client import APIClient
from src.models.api_models import SearchRequest, SearchResponse, ReleaseChangeRequest
from config.settings import settings


class MusicAPIClient(APIClient):
    """Music Catalog API specific client"""
    
    def search(self, search_request: SearchRequest) -> Dict[str, Any]:
        """Perform search request"""
        response = self.post(
            endpoint=f"{settings.API_VERSION}/search",
            data=search_request.dict()
        )
        response.raise_for_status()
        return response.json()
    
    def search_simple(
        self, 
        search_string: str, 
        catalog_ids: List[str] = None,
        user_id: str = None
    ) -> Dict[str, Any]:
        """Simplified search method"""
        request_data = SearchRequest(
            searchString=search_string,
            catalogIds=catalog_ids or ["nugs"],
            userId=user_id
        )
        return self.search(request_data)
    
    def update_releases(self, releases: List[ReleaseChangeRequest]) -> Dict[str, Any]:
        """Update releases via Release Changes endpoint"""
        response = self.post(
            endpoint=f"{settings.API_VERSION}/release-changes",
            data=[release.dict() for release in releases]
        )
        response.raise_for_status()
        return response.json()
    
    def update_release(self, release: ReleaseChangeRequest) -> Dict[str, Any]:
        """Update single release"""
        return self.update_releases([release])
    
    def add_release_favorites(self, user_id: str, release_ids: List[str]) -> Dict[str, Any]:
        """Add releases to user favorites"""
        data = {
            "userId": user_id,
            "releaseIds": release_ids,
            "actionDate": "2024-01-01T00:00:00Z"
        }
        response = self.post(
            endpoint=f"{settings.API_VERSION}/release-favorites/add",
            data=[data]
        )
        response.raise_for_status()
        return response.json()
    
    def add_artist_favorites(self, user_id: str, artist_ids: List[str]) -> Dict[str, Any]:
        """Add artists to user favorites"""
        data = {
            "userId": user_id,
            "artistIds": artist_ids,
            "actionDate": "2024-01-01T00:00:00Z"
        }
        response = self.post(
            endpoint=f"{settings.API_VERSION}/artist-favorites/add",
            data=[data]
        )
        response.raise_for_status()
        return response.json()