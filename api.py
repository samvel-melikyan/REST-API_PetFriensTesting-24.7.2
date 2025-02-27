"""Модуль 19"""
import json

import pytest
import requests
from requests import session
from requests.exceptions import InvalidHeader
from requests_toolbelt import MultipartEncoder
from settings import *
import secrets


class PetFriends:
    """апи библиотека к веб приложению Pet Friends"""

    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email: str, passwd: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
        JSON с уникальным ключем пользователя, найденного по указанным email и паролем"""
        print(f"1111111111111111111111111111111111111111111111111\n{__name__} -111111111111111111111111111111111111111111111111111111111")
        headers = {
            'email': email,
            'password': passwd,
        }
        try:
            res = requests.get(self.base_url + 'api/key', headers=headers)
            status = res.status_code
            result = ""
            try:
                result = res.json()
            except json.decoder.JSONDecodeError:
                result = res.text
        except InvalidHeader or UnboundLocalError:
            status = 403
            result = ""

        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str = "") -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
        со списком наденных питомцев, совпадающих с фильтром. На данный момент фильтр может иметь
        либо пустое значение - получить список всех питомцев, либо 'my_pets' - получить список
        собственных питомцев"""
        try:
            headers = {'auth_key': auth_key['key']}
        except TypeError:
            headers = {'auth_key': auth_key}
        filter = {'filter': filter}
        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str,
                    age: str, pet_photo: str) -> json:
        """Метод отправляет (постит) на сервер данные о добавляемом питомце и возвращает статус
        запроса на сервер и результат в формате JSON с данными добавленного питомца"""
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        try:
            headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        except TypeError:
            headers = {'auth_key': auth_key, 'Content-Type': data.content_type}

        result = ""
        try:
            res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
            status = res.status_code
            try:
                result = res.json()
            except json.decoder.JSONDecodeError:
                result = res.text
        except InvalidHeader or UnboundLocalError:
            status = 403
            result = ""

        print(result)
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает
        статус запроса и результат в формате JSON с текстом уведомления о успешном удалении.
        На сегодняшний день тут есть баг - в result приходит пустая строка, но status при этом = 200"""
        try:
            headers = {'auth_key': auth_key['key']}
        except TypeError:
            headers = {'auth_key': auth_key}
        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, name: str,
                        animal_type: str, age: int) -> json:
        """Метод отправляет запрос на сервер о обновлении данных питомуа по указанному ID и
        возвращает статус запроса и result в формате JSON с обновлённыи данными питомца"""
        try:
            headers = {'auth_key': auth_key['key']}
        except TypeError:
            headers = {'auth_key': auth_key}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
