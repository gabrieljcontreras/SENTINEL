from fastapi.testclient import TestClient

from app.main import app
from app.orchestrators import dataset, agent
from app.dtos.dataset import InspectionDataset

client = TestClient(app)
HEADERS = {"Authorization": "Bearer sentinel-public-dashboard"}


def test_public_dashboard_reads_only_the_shared_workspace(monkeypatch):
    organizations = []

    def read(source, organization_id, detail=True):
        organizations.append(organization_id)
        return InspectionDataset()

    monkeypatch.setattr(dataset, "get_dataset", read)
    response = client.get("/dataset", headers=HEADERS)
    assert response.status_code == 200
    assert organizations == ["org_north"]
    assert client.get("/api/auth/session", headers=HEADERS).json()["organization"]["id"] == "org_north"
    assert client.get("/api/orbit/organizations/org_south/inspections", headers=HEADERS).status_code == 404


def test_public_dashboard_chat_carries_workspace_to_agent(monkeypatch):
    captured = []
    monkeypatch.setattr(agent, "operator_context", lambda user: {"organization_id": user.organization_id})

    def ask(message, session_id, actor, authorization, operator):
        captured.append((authorization, operator["organization_id"]))
        return "Ready."

    monkeypatch.setattr(agent, "ask", ask)
    response = client.post("/api/agent/chat", headers=HEADERS,
                           json={"message": "Help", "session_id": "public-chat-123"})
    assert response.status_code == 200
    assert response.json()["reply"] == "Ready."
    assert captured == [("Bearer sentinel-public-dashboard", "org_north")]


def test_unrecognized_tokens_still_require_a_valid_session():
    assert client.get("/api/auth/session", headers={"Authorization": "Bearer expired"}).status_code == 401
