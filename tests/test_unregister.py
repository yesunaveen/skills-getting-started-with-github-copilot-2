import pytest


class TestUnregisterFromActivity:
    def test_unregister_happy_path(self, client):
        """Happy path: Student successfully unregisters from activity."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered
        
        # Act
        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert "Unregistered" in data["message"]
        assert email in data["message"]
    
    def test_unregister_nonexistent_activity_returns_404(self, client):
        """Error case: Unregistering from non-existent activity returns 404."""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        data = response.json()
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in data["detail"]
    
    def test_unregister_nonparticipant_returns_400(self, client):
        """Error case: Unregistering non-participant returns 400."""
        # Arrange
        activity_name = "Chess Club"
        email = "notasignup@mergington.edu"  # Not registered
        
        # Act
        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        data = response.json()
        
        # Assert
        assert response.status_code == 400
        assert "not signed up" in data["detail"]
    
    def test_unregister_missing_email_parameter_fails(self, client):
        """Error case: Missing email parameter causes request to fail."""
        # Arrange
        activity_name = "Chess Club"
        
        # Act
        response = client.delete(f"/activities/{activity_name}/unregister")
        
        # Assert
        assert response.status_code == 422  # Unprocessable Entity
    
    def test_unregister_removes_participant_from_list(self, client):
        """Integration test: Verify participant is removed from activity's list."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        client.delete(f"/activities/{activity_name}/unregister?email={email}")
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert email not in activities[activity_name]["participants"]
    
    def test_unregister_updates_availability_spots(self, client):
        """Integration test: Verify available spots increases after unregister."""
        # Arrange
        activity_name = "Gym Class"
        email = "john@mergington.edu"
        initial_response = client.get("/activities")
        initial_max = initial_response.json()[activity_name]["max_participants"]
        initial_count = len(initial_response.json()[activity_name]["participants"])
        initial_spots = initial_max - initial_count
        
        # Act
        client.delete(f"/activities/{activity_name}/unregister?email={email}")
        updated_response = client.get("/activities")
        updated_count = len(updated_response.json()[activity_name]["participants"])
        updated_spots = initial_max - updated_count
        
        # Assert
        assert updated_spots == initial_spots + 1
