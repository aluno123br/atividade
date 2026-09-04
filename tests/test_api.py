def create_base_data(client):
    profile = client.post(
        "/api/profiles",
        json={
            "name": "Carlos Silva",
            "bio": "Desenvolvedor backend",
            "email": "carlos@example.com",
            "github_url": "https://github.com/carlos",
            "linkedin_url": "https://www.linkedin.com/in/carlos",
        },
    )
    assert profile.status_code == 201

    tech_python = client.post("/api/technologies", json={"name": "Python"})
    tech_fastapi = client.post("/api/technologies", json={"name": "FastAPI"})
    assert tech_python.status_code == 201
    assert tech_fastapi.status_code == 201

    project = client.post(
        "/api/projects",
        json={
            "title": "DevShowcase",
            "description": "API acadêmica de portfólio.",
            "repository_url": "https://github.com/carlos/devshowcase",
            "profile_id": profile.json()["id"],
            "technology_ids": [tech_python.json()["id"], tech_fastapi.json()["id"]],
        },
    )
    assert project.status_code == 201
    return profile.json(), tech_python.json(), tech_fastapi.json(), project.json()


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_profile_creation_and_lookup(client):
    response = client.post(
        "/api/profiles",
        json={
            "name": "Maria Souza",
            "email": "maria@example.com",
            "github_url": "https://github.com/maria",
        },
    )
    assert response.status_code == 201
    profile_id = response.json()["id"]

    lookup = client.get(f"/api/profiles/{profile_id}")
    assert lookup.status_code == 200
    assert lookup.json()["name"] == "Maria Souza"


def test_technology_listing(client):
    client.post("/api/technologies", json={"name": "PostgreSQL"})
    client.post("/api/technologies", json={"name": "Python"})
    response = client.get("/api/technologies")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_project_filter_and_pagination(client):
    _, _, _, project = create_base_data(client)
    response = client.get("/api/projects?technology=Python&page=0&size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["id"] == project["id"]
    assert data["pages"] == 1


def test_feedback_updates_average(client):
    _, _, _, project = create_base_data(client)
    project_id = project["id"]

    first = client.post(
        f"/api/projects/{project_id}/feedbacks",
        json={"rating": 5, "comment": "Excelente projeto"},
    )
    second = client.post(
        f"/api/projects/{project_id}/feedbacks",
        json={"rating": 3, "comment": "Projeto muito bom"},
    )
    assert first.status_code == 201
    assert second.status_code == 201
    assert second.json()["project_average_rating"] == 4.0


def test_upvote(client):
    _, _, _, project = create_base_data(client)
    response = client.put(f"/api/projects/{project['id']}/upvote")
    assert response.status_code == 200
    assert response.json()["upvotes"] == 1


def test_validation_error_returns_400(client):
    response = client.post(
        "/api/profiles",
        json={
            "name": "A",
            "email": "email-invalido",
            "github_url": "nao-e-url",
        },
    )
    assert response.status_code == 400
    assert response.json()["status"] == 400


def test_not_found_returns_404(client):
    response = client.get("/api/profiles/999999")
    assert response.status_code == 404
    assert response.json()["status"] == 404
