import allure
import json


def attach_request_resp(response):
    request = response.request

    allure.attach(request.method, name="Метод запроса", attachment_type=allure.attachment_type.TEXT)
    allure.attach(request.url, name="URL запроса", attachment_type=allure.attachment_type.TEXT)

    if request.headers:
        allure.attach(json.dumps(dict(request.headers), indent=4, ensure_ascii=False),
                      name="Header запроса", attachment_type=allure.attachment_type.JSON)

    if request.body:
        try:
            parsed_body = json.loads(request.body)
            allure.attach(json.dumps(parsed_body, indent=4, ensure_ascii=False),
                          name="Body запроса", attachment_type=allure.attachment_type.JSON)
        except TypeError:
            allure.attach(str(request.body), name="Body запроса",
                          attachment_type=allure.attachment_type.TEXT)

    allure.attach(str(response.status_code), name="Status ответа",
                  attachment_type=allure.attachment_type.TEXT)

    if response.headers:
        allure.attach(json.dumps(dict(response.headers), indent=4, ensure_ascii=False),
                      name="Header ответа", attachment_type=allure.attachment_type.JSON)

    try:
        allure.attach(json.dumps(response.json(), indent=4, ensure_ascii=False),
                      name="Body ответа", attachment_type=allure.attachment_type.JSON)
    except TypeError:
        allure.attach(response.text, name="Body ответа",
                      attachment_type=allure.attachment_type.TEXT)
