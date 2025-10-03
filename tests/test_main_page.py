import pytest
import requests
import json
from utils.main_page.api import get_active_items, get_cart, add_to_cart
import allure
from utils.functions import attach_request_resp


@allure.parent_suite('Главная страница')
@allure.suite('Проверка добавления товара в корзину у незарегистрированного пользователя')
@allure.title('Получение товаров')
def test_get_active_item():
    global offer_id, slug, condition_id

    with allure.step('Отправка запроса на получение товара'):
        response = get_active_items()
        attach_request_resp(response)

    with allure.step('Проверка статуса ответа'):
        assert response.status_code == 200

    response = response.json()
    with allure.step('Проверка что в ответе есть товары'):
        assert len(response) > 1

    first_item = response[0]['offers'][0]

    offer_id = first_item['moderated_offer_id']
    slug = first_item['slug']
    condition_id = first_item['condition']['id']


@allure.parent_suite('Главная страница')
@allure.suite('Проверка добавления товара в корзину у незарегистрированного пользователя')
@allure.title('Получение  session_id из куки')
def test_get_session_id():
    global cookie

    with allure.step('Отправка запроса на получение корзины'):
        response = get_cart()
        attach_request_resp(response=response)

    with allure.step('Проверка статуса ответа'):
        assert response.status_code == 200

    with allure.step('Получение session_id из куки'):
        cookie = response.cookies.get_dict()['cart']
        assert isinstance(cookie, str), f'Тип куки на самом деле {type(cookie)}'


@allure.parent_suite('Главная страница')
@allure.suite('Проверка добавления товара в корзину у незарегистрированного пользователя')
@allure.title('Добавление товара в корзину')
def test_add_item():
    with allure.step('Отправка запроса на добавление товара в корзину'):
        response = add_to_cart(cookie=cookie, offer_id=offer_id, condition_id=condition_id)
        attach_request_resp(response)

    with allure.step('Проверка статуса ответа'):
        assert response.status_code == 200

    with allure.step('Получение ответ добавления товара в корзину'):
        response = response.json()
        print(json.dumps(response, indent=4))




@allure.parent_suite('Главная страница')
@allure.suite('Проверка добавления товара в корзину у незарегистрированного пользователя')
@allure.title('Проверка корзины на товар')
def test_cart_check():
    with allure.step('Отправка запроса на проверку наличия товара в корзине'):
        response = get_cart(cookie=cookie)
        attach_request_resp(response)

    with allure.step('Проверка статуса ответа'):
        assert response.status_code == 200

    with allure.step('Получение ответа наличия товара в корзине'):
        data = response.json()
        print(data)
        assert 'moderated_cart_items' in data, "Ответ корзины не содержит ключ 'moderated_cart_items'"
        assert len(data["moderated_cart_items"]) > 0, "Корзина пустая после добавления товара"

        item = data["moderated_cart_items"][0]
        assert item["moderated_offer_id"] == offer_id, \
            f"Ожидался offer_id={offer_id}, но в корзине {item['moderated_offer_id']}"



# @pytest.mark.parametrize('item', ['iPhone', 'samsung', '8716248712648712648172648127','xiaomi'])
# def test_search(item):
#     search_body = {
#         "query": item
#     }
#
#     response = requests.post(url=search_url, json=search_body)
#     res_json = response.json()
#
#     items_list = res_json["items"]
#
#     print(f'{items_list}\n\n')
#
#     assert response.status_code == 200
#     assert len(items_list) > 0, "Ничего не нашлось"


# def url_generator(slug):
#     return f'{get_item}/{slug}'


# def test_active_items():
#     global item_slug
#
#     response = requests.get(url=active_items_url)
#
#     assert response.status_code == 200
#
#     response = response.json()
#
#     item_slug = response[0]['offers'][0]['slug']
#     print(item_slug)
#
#
# def test_get_item():
#     url = url_generator(item_slug)
#
#     response = requests.get(url=url)
#
#     print(response.json())

