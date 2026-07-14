from services.api.app.main import app


def test_openapi_contains_health_contract() -> None:
    schema = app.openapi()

    operation = schema["paths"]["/health"]["get"]
    assert operation["operationId"] == "getHealth"
    assert (
        operation["responses"]["200"]["content"]["application/json"]["schema"]["$ref"]
        == "#/components/schemas/HealthResponse"
    )
