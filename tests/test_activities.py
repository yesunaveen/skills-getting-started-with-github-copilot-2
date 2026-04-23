import pytest


class TestGetActivities:
    def test_get_all_activities_happy_path(self, client):
        """Happy path: GET /activities returns all activities with correct structure."""
        # Arrange
        expected_activity_names = {"Chess Club", "Programming Class", "Gym Class"}
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert set(data.keys()) == expected_activity_names
    
    def test_activity_has_required_fields(self, client):
        """Edge case: Each activity contains all required fields."""
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_name, activity_data in activities.items():
            assert required_fields.issubset(activity_data.keys()), \
                f"Activity '{activity_name}' missing required fields"
    
    def test_participants_is_list(self, client):
        """Edge case: participants field is always a list."""
        # Arrange & Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["participants"], list), \
                f"Activity '{activity_name}' participants should be a list"
    
    def test_max_participants_is_positive_integer(self, client):
        """Edge case: max_participants is a positive integer."""
        # Arrange & Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["max_participants"], int), \
                f"Activity '{activity_name}' max_participants should be an integer"
            assert activity_data["max_participants"] > 0, \
                f"Activity '{activity_name}' max_participants should be positive"
