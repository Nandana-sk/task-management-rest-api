
import pytest

from app import create_app


@pytest.fixture
def client(tmp_path):
    database_path = tmp_path / "test_tasks.db"

    app = create_app(str(database_path))
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


def test_get_tasks(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.get_json() == {"tasks": []}


def test_create_task(client):
    response = client.post(
        "/tasks",
        json={"title": "Test task"}
    )

    assert response.status_code == 201
    assert response.get_json()["title"] == "Test task"
    assert response.get_json()["completed"] is False


def test_create_task_with_empty_title(client):
    response = client.post(
        "/tasks",
        json={"title": "   "}
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Title is required"


def test_update_task(client):
    created = client.post(
        "/tasks",
        json={"title": "Original task"}
    )

    task_id = created.get_json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={"completed": True}
    )

    assert response.status_code == 200
    assert response.get_json()["completed"] is True
    assert response.get_json()["title"] == "Original task"


def test_update_missing_task(client):
    response = client.put(
        "/tasks/999",
        json={"title": "Updated task"}
    )

    assert response.status_code == 404


def test_delete_task(client):
    created = client.post(
        "/tasks",
        json={"title": "Task to delete"}
    )

    task_id = created.get_json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 204

    remaining = client.get("/tasks").get_json()["tasks"]

    assert all(task["id"] != task_id for task in remaining)


def test_delete_missing_task(client):
    response = client.delete("/tasks/999")

    assert response.status_code == 404
