from services.api.app.main import app


def test_openapi_contains_health_contract() -> None:
    schema = app.openapi()

    operation = schema["paths"]["/health"]["get"]
    assert operation["operationId"] == "getHealth"
    assert (
        operation["responses"]["200"]["content"]["application/json"]["schema"]["$ref"]
        == "#/components/schemas/HealthResponse"
    )


def test_openapi_contains_retrieval_contract() -> None:
    schema = app.openapi()

    operation = schema["paths"]["/api/v1/search"]["post"]
    assert operation["operationId"] == "searchApprovedSources"
    assert (
        operation["requestBody"]["content"]["application/json"]["schema"]["$ref"]
        == "#/components/schemas/SearchRequest"
    )
    assert (
        operation["responses"]["200"]["content"]["application/json"]["schema"]["$ref"]
        == "#/components/schemas/SearchResponse"
    )
