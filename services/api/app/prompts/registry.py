from datetime import date

from pydantic import BaseModel, ConfigDict


class PromptMetadata(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    prompt_id: str
    version: str
    purpose: str
    input_schema: str
    output_schema: str
    owner: str
    created_at: date
    evaluation_set: str
    status: str


GROUNDED_ANSWER_PROMPT = PromptMetadata(
    prompt_id="grounded-answer",
    version="1.0.0",
    purpose="Compose source-grounded historical and symbolic answers.",
    input_schema="GroundedContext",
    output_schema="ProviderAnswer",
    owner="Denge Atlasi",
    created_at=date(2026, 7, 13),
    evaluation_set="sprint04-safety",
    status="TEST_ONLY",
)
