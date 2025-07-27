import pytest
from httpx import AsyncClient
from fastapi import status
from app.main import app

@pytest.mark.asyncio
async def test_get_providers():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/api/scenarios/providers")
        assert resp.status_code == 200
        assert "providers" in resp.json()

@pytest.mark.asyncio
async def test_generate_valid():
    payload = {
        "company_name": "TestCo",
        "industry": "Finance",
        "company_size": "medium",
        "technologies": ["AWS"],
        "threat_actor": "ransomware",
        "scenario_type": "ransomware",
        "participants": ["Security Team"],
        "duration_hours": 2
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/api/scenarios/generate", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert "scenario" in data
        assert "id" in data

@pytest.mark.asyncio
async def test_generate_invalid():
    payload = {
        # missing required fields
        "company_name": "TestCo"
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/api/scenarios/generate", json=payload)
        assert resp.status_code == 422

@pytest.mark.asyncio
async def test_generate_with_competitor_threat_actor():
    payload = {
        "company_name": "TestCo",
        "industry": "Technology",
        "company_size": "medium",
        "technologies": ["AWS", "Kubernetes"],
        "threat_actor": "competitor",
        "scenario_type": "espionage",
        "participants": ["Security Team", "Legal Team"],
        "duration_hours": 2
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/api/scenarios/generate", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert "scenario" in data
        assert "id" in data

@pytest.mark.asyncio
async def test_estimate_cost():
    payload = {
        "company_name": "TestCo",
        "industry": "Finance",
        "company_size": "medium",
        "technologies": ["AWS"],
        "threat_actor": "ransomware",
        "scenario_type": "ransomware",
        "participants": ["Security Team"],
        "duration_hours": 2
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/api/scenarios/estimate-cost", json=payload)
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

@pytest.mark.asyncio
async def test_reroll_section():
    # First, generate a scenario
    payload = {
        "company_name": "TestCo",
        "industry": "Finance",
        "company_size": "medium",
        "technologies": ["AWS"],
        "threat_actor": "ransomware",
        "scenario_type": "ransomware",
        "participants": ["Security Team"],
        "duration_hours": 2
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        gen_resp = await ac.post("/api/scenarios/generate", json=payload)
        assert gen_resp.status_code == 200
        scenario = gen_resp.json()["scenario"]
        reroll_payload = {
            "original_scenario": scenario,
            "section_title": "Initial Compromise",
            "section_content": "Old content",
            "context": payload,
            "llm_provider": None
        }
        reroll_resp = await ac.post("/api/scenarios/reroll", json=reroll_payload)
        assert reroll_resp.status_code == 200
        assert "new_content" in reroll_resp.json()

@pytest.mark.asyncio
async def test_history_endpoints():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Generate a scenario to ensure history is not empty
        payload = {
            "company_name": "TestCo",
            "industry": "Finance",
            "company_size": "medium",
            "technologies": ["AWS"],
            "threat_actor": "ransomware",
            "scenario_type": "ransomware",
            "participants": ["Security Team"],
            "duration_hours": 2
        }
        await ac.post("/api/scenarios/generate", json=payload)
        # Get history
        resp = await ac.get("/api/scenarios/history")
        assert resp.status_code == 200
        history = resp.json()
        assert isinstance(history, list)
        if history:
            # Delete the first scenario
            del_resp = await ac.delete(f"/api/scenarios/history/{history[0]['id']}")
            assert del_resp.status_code == 200
            assert del_resp.json().get("success") 