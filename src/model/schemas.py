from pydantic import BaseModel, Field


class QaseData(BaseModel):
    qase_number_test_cases: list[int]
    qase_token: str
    qase_url: str = Field(default="https://api.qase.io")
    project_name: str
    testit_projectId: str
    testit_sectionId: str
