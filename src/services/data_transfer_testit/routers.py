from typing import Optional

from fastapi import APIRouter, File, UploadFile, Form, HTTPException

from src.schemas.schemas import QaseData
from src.services.data_transfer_testit.scripts import data_from_qase, send_data_to_testit

router_migration = APIRouter(
    prefix="/migration",
    tags=["migration"]
)


@router_migration.post("/from_qase_to_testit")
def get_prepare_data_from_qase(qase_data: QaseData):
    """
    Метод для получения и обработки данных по TestCase из Qase и запись их в json файл для отправки в TestIt.
    :param qase_data: Данные Qase(Набор кейсов,
                                  API токен доступа из QASE,
                                  URL API из QASE,
                                  имя проекта в QASE,
                                  ID проекта в TESTIT,
                                  ID секции  в TESTIT)
    :return: Json файл с данными для отправки в TestIt.
    """
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
    '''
    Метод для создание TestCase в TestIt по данным из json файла.
    :param testit_token : API токен доступа в TestIt.
    :param testit_cookies : Cookies для авторизации в TestIt.
    :param testit_url : URL API в TestIt.
    :param file : Json файл с данными для отправки в TestIt полученный в ответе на запрос /from_qase_to_testit.
    :return: Список id созданных TestCase в TestIt.
    '''
    try:
        return await send_data_to_testit(file, testit_token, testit_cookies, testit_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")
