from pydantic import BaseModel, Field


class ReportDataV2(BaseModel):
    qase_url: str | None
    qase_number_test_cases: list[int]
    qase_token: str
    qase_project_name: str
    testit_token: str
    testit_cookies: str | None
    testit_projectId: str
    testit_sectionId: str
    testit_url: str


class ReportData(BaseModel):
    number_test_cases: list[int]
    qase_cookies: str
    qase_x_xsfr_token: str
    project_name: str
    testit_token: str
    testit_cookies: str | None
    testit_projectId: str
    testit_sectionId: str
    url_testit: str


class QaseData(BaseModel):
    qase_number_test_cases: list[int]
    qase_token: str
    qase_url: str = Field(default="https://api.qase.io")
    project_name: str
    testit_projectId: str
    testit_sectionId: str


class TestItData(BaseModel):
    testit_token: str
    testit_cookies: str | None
    url_testit: str
