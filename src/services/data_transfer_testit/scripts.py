import json
import os
import time
import requests

from fastapi.responses import FileResponse
from fastapi import UploadFile, HTTPException


def formation_steps(test_run_steps):
    testit_testcase_steps = []

    for step in test_run_steps:
        testit_testcase_step = {
            "action": f"<p class=\"tiptap-text\">{step['action']}</p>",
            "expected": f"<p class=\"tiptap-text\">{step['expected_result']}</p>",
            "testData": f"<p class=\"tiptap-text\">{step['data']}</p>",
            "comments": ""
        }
        testit_testcase_steps.append(testit_testcase_step)

    return testit_testcase_steps


def data_from_qase(qase_data):
    headers_qase = {
        "Token": f"{qase_data.qase_token}",
        "accept": "application/json"}

    data_from_qase_json = []

    for case in qase_data.qase_number_test_cases:
        url = f'{qase_data.qase_url}/v1/case/{qase_data.project_name}/{int(case)}'

        responce_qase_testcase = requests.get(url, headers=headers_qase)

        responce_qase_testcase_json = responce_qase_testcase.json()

        test_run_steps = responce_qase_testcase_json['result']['steps']

        testit_testcase_steps = formation_steps(test_run_steps)

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
        return FileResponse(file_path, media_type='application/octet-stream', filename=file_name)
    else:
        raise HTTPException(status_code=431, detail="File not found")


async def send_data_to_testit(file: UploadFile, testit_token, testit_cookies, testit_url):
    testit_testcase_ids = []

    contents = await file.read()

    qase_data_json = json.loads(contents.decode("utf-8"))

    url = f'{testit_url}/api/v2/WorkItems'

    headers = {
        "Authorization": f"{testit_token}",
        "Cookie": f"{testit_cookies}"
    }

    for case in qase_data_json:

        responce_testcase = requests.post(url, headers=headers, json=case)

        if responce_testcase.status_code == 201:
            testit_testcase = responce_testcase.json()
            testit_testcase_ids.append(testit_testcase['id'])
        if responce_testcase.status_code != 201:
            raise HTTPException(status_code=500,
                                detail=f"Импорт прерван {responce_testcase.status_code}. Перенесённые кейсы: {testit_testcase_ids}")

    return testit_testcase_ids
