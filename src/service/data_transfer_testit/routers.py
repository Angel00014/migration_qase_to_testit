from typing import Optional

from fastapi import APIRouter, File, UploadFile, Form, HTTPException

from src.model.schemas import QaseData
from src.service.data_transfer_testit.scripts import data_from_qase, send_data_to_testit

router_migration = APIRouter(
    prefix="/migration",
    tags=["migration"]
)


@router_migration.post("/from_qase_to_testit")
def get_prepare_data_from_qase(qase_data: QaseData):
    try:
        return data_from_qase(qase_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка: {str(e)}")


@router_migration.post("/testcases_to_testit")
async def load_prepare_data_to_testit(
        testit_token: str = Form(...),
        testit_cookies: Optional[str] = Form(None),
        testit_url: str = Form(...),
        file: UploadFile = File(...)):
    try:
        return await send_data_to_testit(file, testit_token, testit_cookies, testit_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")
