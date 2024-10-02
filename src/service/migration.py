import json
import os
import time
from typing import Optional
import logging

import requests

from fastapi import FastAPI, APIRouter, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from src.model.baseModel import ReportData, QaseData, TestItData, ReportDataV2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router_migration = APIRouter(
    prefix="/migration",
    tags=["migration"]
)

logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")


# Функция скрыта. Необходимо сделать рефакторинг
# def get_qase_data(report_data):
#     try:
#         headers_qase = {
#             "Token": f"{report_data.qase_token}",
#             "accept": "application/json"
#         }
#         testit_testcase_steps = []
#         responce_qase_testcase_json = ''
#         for case in report_data.qase_number_test_cases:
#             if report_data.qase_url == "" or report_data.qase_url is None:
#                 report_data.qase_url = f'https://api.qase.io'
#
#             url = f"{report_data.qase_url}/v1/case/{report_data.qase_project_name}/{int(case)}"
#
#             responce_qase_testcase = requests.get(url, headers=headers_qase)
#
#             responce_qase_testcase_json = responce_qase_testcase.json()
#
#             test_run_steps = responce_qase_testcase_json['result']['steps']
#
#             logging.error(responce_qase_testcase)
#
#             for step in test_run_steps:
#                 # if step['shared'] == "":
#                 testit_testcase_step = {
#                     "action": f"<p class=\"tiptap-text\">{step['action']}</p>",
#                     "expected": f"<p class=\"tiptap-text\">{step['expected_result']}</p>",
#                     "testData": f"<p class=\"tiptap-text\">{step['data']}</p>",
#                     "comments": ""
#                 }
#                 testit_testcase_steps.append(testit_testcase_step)
#                 # elif step['shared'] != "":
#                 #     url = f'https://app.qase.io/v1/shared_step/{report_data.qase_project_name}/{step['shared']}'
#                 #
#                 #     responce_shared = requests.get(url, headers=headers_qase)
#                 #
#                 #     responce_shared_json = responce_shared.json()
#                 #
#                 #     for shared_step in responce_shared_json['result']['steps']:
#                 #         testit_testcase_step = {
#                 #             "action": f"<p class=\"tiptap-text\">{shared_step['action']}</p>",
#                 #             "expected": f"<p class=\"tiptap-text\">{shared_step['expected_result']}</p>",
#                 #             "testData": f"<p class=\"tiptap-text\">{shared_step['data']}</p>",
#                 #             "comments": ""
#                 #         }
#                 #         testit_testcase_steps.append(testit_testcase_step)
#         if responce_qase_testcase_json is None or responce_qase_testcase_json == '':
#             return False
#         else:
#             return testit_testcase_steps, responce_qase_testcase_json
#
#     except Exception as e:
#         print(e, url, responce_qase_testcase.status_code)

# Метод скрыт. Необходимо полностью переписать метод
# @router_migration.post("/migration_qase_testIt")
# def migration_qase_testIt(report_data: ReportDataV2):
#     try:
#         # headers_qase = {
#         #     "Cookie": f"{report_data.qase_cookies}",
#         #     "X-Xsrf-Token": f"{report_data.qase_x_xsfr_token}",
#         #     "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
#         # }
#         #
#         # testit_testcase_ids = []
#         #
#         # for case in report_data.number_test_cases:
#         #
#         #     url = f'https://app.qase.io/v2/case/load'
#         #
#         #     body = {
#         #         "code": f"{report_data.project_name}",
#         #         "id": f"{int(case)}"
#         #     }
#         #
#         #     responce_dashboard = requests.post(url, headers=headers_qase, json=body)
#         #
#         #     responce_dashboard_json = responce_dashboard.json()
#         #
#         #     test_run_steps = responce_dashboard_json['case']['steps']
#         #
#         #     testit_testcase_steps = []
#         #     for step in test_run_steps:
#         #         if step['shared'] == "":
#         #             testit_testcase_step = {
#         #                 "action": f"<p class=\"tiptap-text\">{step['action']}</p>",
#         #                 "expected": f"<p class=\"tiptap-text\">{step['expected_result']}</p>",
#         #                 "testData": f"<p class=\"tiptap-text\">{step['data']}</p>",
#         #                 "comments": ""
#         #             }
#         #             testit_testcase_steps.append(testit_testcase_step)
#         #         elif step['shared'] != "":
#         #             url = f'https://app.qase.io/v1/step/{report_data.project_name}/load'
#         #
#         #             body = {
#         #                 "hash": step['shared']
#         #             }
#         #
#         #             responce_shared = requests.post(url, headers=headers_qase, json=body)
#         #
#         #             responce_shared_json = responce_shared.json()
#         #
#         #             for shared_step in responce_shared_json['step']['steps']:
#         #                 testit_testcase_step = {
#         #                     "action": f"<p class=\"tiptap-text\">{shared_step['action']}</p>",
#         #                     "expected": f"<p class=\"tiptap-text\">{shared_step['expected_result']}</p>",
#         #                     "testData": f"<p class=\"tiptap-text\">{shared_step['data']}</p>",
#         #                     "comments": ""
#         #                 }
#         #                 testit_testcase_steps.append(testit_testcase_step)
#         testit_testcase_ids = []
#
#         get_qase_data(report_data)
#
#         if get_qase_data(report_data) == False or get_qase_data(report_data) is None:
#             return "Данные из QASE не были получены"
#         else:
#             testit_testcase_steps, responce_qase_testcase_json = get_qase_data(report_data)
#
#         body_case_testit = {
#             "name": responce_qase_testcase_json['result']['title'],
#             "entityTypeName": "TestCases",
#             "attachments": [],
#             "projectId": report_data.testit_projectId,
#             "duration": 600000,
#             "tags": [],
#             "state": "NotReady",
#             "priority": "Medium",
#             "description": responce_qase_testcase_json['result']['description'],
#             "steps": testit_testcase_steps,
#             "preconditionSteps": [
#                 {
#                     "action": f"<p class=\"tiptap-text\">{responce_qase_testcase_json['result']['preconditions']}</p>",
#                     "expected": "",
#                     "testData": "",
#                     "comments": ""
#                 }
#             ],
#             "postconditionSteps": [
#                 {
#                     "action": f"<p class=\"tiptap-text\">{responce_qase_testcase_json['result']['postconditions']}</p>",
#                     "expected": "",
#                     "testData": "",
#                     "comments": ""
#                 }
#             ],
#             "iterations": [],
#             "links": [],
#             "autoTests": [],
#             "sectionId": report_data.testit_sectionId,
#             "attributes": {}
#         }
#
#         url = f'{report_data.testit_url}/api/v2/WorkItems'
#
#         headers = {
#             "Authorization": f"{report_data.testit_token}"
#         }
#
#         responce_testcase = requests.post(url, headers=headers, json=body_case_testit)
#
#         if responce_testcase.status_code == 201:
#             testit_testcase = responce_testcase.json()
#             testit_testcase_ids.append(testit_testcase['id'])
#
#         logging.debug(f"{responce_testcase.status_code}")
#         return body_case_testit
#
#     except Exception as e:
#         print(e, body_case_testit)


@router_migration.post("/from_qase_to_testit")
def get_prepare_data_from_qase(qase_data: QaseData):
    try:
        headers_qase = {
            "Token": f"{qase_data.qase_token}",
            "accept": "application/json"}

        data_from_qase_json = []

        for case in qase_data.qase_number_test_cases:

            url = f'{qase_data.qase_url}/v1/case/{qase_data.project_name}/{int(case)}'

            responce_qase_testcase = requests.get(url, headers=headers_qase)

            responce_qase_testcase_json = responce_qase_testcase.json()

            test_run_steps = responce_qase_testcase_json['result']['steps']

            testit_testcase_steps = []
            for step in test_run_steps:
                testit_testcase_step = {
                    "action": f"<p class=\"tiptap-text\">{step['action']}</p>",
                    "expected": f"<p class=\"tiptap-text\">{step['expected_result']}</p>",
                    "testData": f"<p class=\"tiptap-text\">{step['data']}</p>",
                    "comments": ""
                }
                testit_testcase_steps.append(testit_testcase_step)

            body_case_testit = {
                "name": responce_qase_testcase_json['result']['title'],
                "entityTypeName": "TestCases",
                "attachments": [],
                "projectId": qase_data.testit_projectId,
                "duration": 600000,
                "tags": [],
                "state": "NotReady",
                "priority": "Medium",
                "description": responce_qase_testcase_json['result']['description'],
                "steps": testit_testcase_steps,
                "preconditionSteps": [
                    {
                        "action": f"<p class=\"tiptap-text\">{responce_qase_testcase_json['result']['preconditions']}</p>",
                        "expected": "",
                        "testData": "",
                        "comments": ""
                    }
                ],
                "postconditionSteps": [
                    {
                        "action": f"<p class=\"tiptap-text\">{responce_qase_testcase_json['result']['postconditions']}</p>",
                        "expected": "",
                        "testData": "",
                        "comments": ""
                    }
                ],
                "iterations": [],
                "links": [],
                "autoTests": [],
                "sectionId": qase_data.testit_sectionId,
                "attributes": {}
            }

            data_from_qase_json.append(body_case_testit)

        timestamp = int(time.time())

        base_folder = "file"
        os.makedirs(base_folder, exist_ok=True)

        file_name = f'json_{timestamp}.json'
        file_path = os.path.join(base_folder, file_name)

        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            json.dump(data_from_qase_json, file, ensure_ascii=False, indent=4)

        if os.path.exists(file_path):
            # Возвращаем файл для скачивания
            return FileResponse(file_path, media_type='application/octet-stream', filename=file_name)
        else:
            raise HTTPException(status_code=431, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка: {str(e)}")


@router_migration.post("/testcases_to_testit")
async def load_prepare_data_to_testit(
        testit_token: str = Form(...),
        testit_cookies: Optional[str] = Form(None),
        testit_url: str = Form(...),
        file: UploadFile = File(...)):
    try:

        testit_testcase_ids = []

        contents = await file.read()

        qase_data_json = json.loads(contents.decode("utf-8"))

        for case in qase_data_json:
            url = f'{testit_url}/api/v2/WorkItems'

            headers = {
                "Authorization": f"{testit_token}",
                "Cookie": f"{testit_cookies}"
            }

            responce_testcase = requests.post(url, headers=headers, json=case)

            if responce_testcase.status_code == 201:
                testit_testcase = responce_testcase.json()
                testit_testcase_ids.append(testit_testcase['id'])
            if responce_testcase.status_code != 201:
                raise HTTPException(status_code=500,
                                    detail=f"Импорт прерван {responce_testcase.status_code}. Перенесённые кейсы: {testit_testcase_ids}")

        return testit_testcase_ids


    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")
