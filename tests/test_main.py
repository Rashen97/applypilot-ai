from fastapi.testclient import TestClient
from backend.app.main import app


client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_job():
    response = client.post("/jobs", json={"title": "Software Engineer", "company": "Tech Corp"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Software Engineer" 
    assert data["company"] == "Tech Corp"
    assert "id" in data  # Ensure the response contains an ID

def test_get_jobs():
    response = client.get("/jobs")

    assert response.status_code == 200
    assert response.json() == []  # Initially, the database should be empty
    data = response.json()

    assert isinstance(data, list)

def test_get_job():
    create_response = client.post(
        "/jobs",
        json={
            "title": "Backend Developer",
            "company": "Test Company"
        }
    )

    job_id = create_response.json()["id"]

    response = client.get(f"/jobs/{job_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == job_id
    assert data["title"] == "Backend Developer"
    assert data["company"] == "Test Company"

def test_get_job_not_found():
    response = client.get("/jobs/99999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Job not found"}

def test_update_job():
    create_response = client.post(
        "/jobs",
        json={
            "title": "Python Developer",
            "company": "Original Company"
        }
    )

    job_id = create_response.json()["id"]

    response = client.patch(
        f"/jobs/{job_id}",
        json={
            "title": "AI Engineer"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "AI Engineer"
    assert data["company"] == "Original Company"

def test_update_job_not_found():
    response = client.patch(
        "/jobs/99999",
        json={
            "title": "AI Engineer"
        }
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Job not found"}

def test_delete_job():
    create_response = client.post(
        "/jobs",
        json={
            "title": "Delete Me",
            "company": "Test Company"
        }
    )

    job_id = create_response.json()["id"]

    response = client.delete(f"/jobs/{job_id}")

    assert response.status_code == 204

    get_response = client.get(f"/jobs/{job_id}")

    assert get_response.status_code == 404

def test_delete_job_not_found():
    response = client.delete("/jobs/99999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Job not found"}

def test_create_job_missing_company():
    response = client.post(
        "/jobs",
        json={
            "title": "Software Engineer"
        }
    )

    assert response.status_code == 422