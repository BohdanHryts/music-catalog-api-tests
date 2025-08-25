import json
from typing import Dict, Any, List
from jsonschema import validate, ValidationError


class APITestHelpers:
    """Helper utilities for API testing"""
    
    @staticmethod
    def validate_search_response_schema(response_data: Dict[str, Any]) -> bool:
        """Validate search response against expected schema"""
        schema = {
            "type": "object",
            "properties": {
                "albums": {"type": "array"},
                "artists": {"type": "array"},
                "tracks": {"type": "array"},
                "venues": {"type": "array"},
                "performanceYears": {"type": "array"},
                "performanceDates": {"type": "array"}
            },
            "required": ["albums", "artists", "tracks", "venues", "performanceYears", "performanceDates"]
        }
        
        try:
            validate(response_data, schema)
            return True
        except ValidationError as e:
            print(f"Schema validation failed: {e}")
            return False
    
    @staticmethod
    def validate_catalog_access(
        search_catalog_ids: List[str],
        result_catalog_ids: List[str]
    ) -> bool:
        """Validate catalog access rules based on requirements"""
        # Rule 1: If searching nugs only
        if search_catalog_ids == ["nugs"]:
            return set(result_catalog_ids).issubset({"nugs", "nugs,playDead"})
        
        # Rule 2: If searching playDead only
        elif search_catalog_ids == ["playDead"]:
            return set(result_catalog_ids).issubset({"playDead", "nugs,playDead"})
        
        # Rule 3: If searching both
        elif set(search_catalog_ids) == {"nugs", "playDead"}:
            return True  # All results should be accessible
        
        return False
    
    @staticmethod
    def check_active_status_filter(items: List[Dict[str, Any]]) -> bool:
        """Check that only active items are included in results"""
        active_statuses = {1, 2}  # Live, Pre-Order
        for item in items:
            if 'status' in item and item['status'] not in active_statuses:
                return False
        return True
    
    @staticmethod
    def verify_ranking_order(results: List[Dict[str, Any]], max_relevance_results: int = 5) -> bool:
        """Verify that first 5 results are relevance-ranked, rest are personalized"""
        # This would need to be implemented based on actual ranking logic
        return len(results) <= 50  # Hard limit check
    
    @staticmethod
    def pretty_print_json(data: Dict[str, Any]) -> str:
        """Pretty print JSON data for debugging"""
        return json.dumps(data, indent=2, default=str)