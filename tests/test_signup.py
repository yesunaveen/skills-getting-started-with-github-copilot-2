import pytest


class TestSignupForActivity:
    def test_signup_happy_path(self, client):
        """Happy path: Student successfully signs up for activity."""
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert "Signed up" in data["message"]
        assert email in data["message"]
    
    def test_signup_nonexistent_activity_returns_404(self, client):
        """Error case: Signing up for non-existent activity returns 404."""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        data = response.json()
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in data["detail"]
    
    def test_signup_duplicate_email_returns_400(self, client):
        """Error case: Signing up twice with same email returns 400."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        data = response.json()
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in data["detail"]
    
    def test_signup_missing_email_parameter_fails(self, client):
        """Error case: Missing email parameter causes request to fail."""
        # Arrange
        activity_name = "Chess Club"
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup")
        
        # Assert
        assert response.status_code == 422  # Unprocessable Entity
    
    def test_signup_adds_participant_to_list(self, client):
        """Integration test: Verify participant is added to activity's participants list."""
        # Arrange
        activity_name = "Programming Class"
        email = "newsignup@mergington.edu"
        
        # Act
        client.post(f"/activities/{activity_name}/signup?email={email}")
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert email in activities[activity_name]["participants"]
    
    def test_signup_updates_availability_spots(self, client):
        """Integration test: Verify available spots decreases after signup."""
        # Arrange
        activity_name = "Gym Class"
        initial_response = client.get("/activities")
        initial_max = initial_response.json()[activity_name]["max_participants"]
        initial_count = len(initial_response.json()[activity_name]["participants"])
        initial_spots = initial_max - initial_count
        
        # Act
        email = "newstudent@mergington.edu"
        client.post(f"/activities/{activity_name}/signup?email={email}")
        updated_response = client.get("/activities")
        updated_count = len(updated_response.json()[activity_name]["participants"])
        updated_spots = initial_max - updated_count
        
        # Assert
        assert updated_spots == initial_spots - 1
