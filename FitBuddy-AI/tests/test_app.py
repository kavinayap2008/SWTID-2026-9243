import os


# ---------------------------------------------------------
# TEST ENVIRONMENT
# ---------------------------------------------------------

os.environ["MOCK_AI"] = "true"

os.environ[
    "DATABASE_URL"
] = "sqlite:///./test_fitbuddy.db"


from fastapi.testclient import TestClient

from app.main import app


# ---------------------------------------------------------
# END-TO-END TEST
# ---------------------------------------------------------

def test_health_and_workout_flow():

    with TestClient(app) as client:

        # -----------------------------------------------
        # HEALTH
        # -----------------------------------------------

        health = client.get(
            "/health"
        )

        assert health.status_code == 200


        # -----------------------------------------------
        # CREATE WORKOUT
        # -----------------------------------------------

        payload = {

            "user_id": 9001,

            "username":
                "Demo User",

            "age": 30,

            "weight": 70,

            "goal":
                "general wellness",

            "intensity":
                "medium",
        }


        response = client.post(
            "/api/workouts",
            json=payload,
        )


        assert response.status_code == 200


        data = response.json()


        assert (
            "Day 7"
            in data["workout_plan"]
        )


        # -----------------------------------------------
        # FEEDBACK
        # -----------------------------------------------

        feedback = client.post(

            "/api/feedback",

            json={

                "user_id":
                    9001,

                "feedback":
                    "Add more mobility",
            },
        )


        assert feedback.status_code == 200


        # -----------------------------------------------
        # USERS
        # -----------------------------------------------

        users = client.get(
            "/api/users"
        )


        assert users.status_code == 200


        assert any(

            user["user_id"] == 9001

            for user in users.json()
        )