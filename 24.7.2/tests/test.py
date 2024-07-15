import os.path
import pytest
from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password

pf = PetFriends()


def test_get_api_key_valid_user(emai=valid_email, password=valid_password):
    status, result = pf.get_api_key(emai, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_create_pet_simple(name='', animal_type='', age='', pet_photo=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, 'my_pets')
    _, my_pet = pf.get_list_of_pets(auth_key, "my_pets")

    assert status != 400


def test_add_new_pet_with_valid_data(name='Slon', animal_type='dog', age='3'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == 'Slon'
    assert result['animal_type'] == 'dog'
    assert result['age'] == '3'


#проверка невалидного пароля
def test_get_api_key_for_invalid_user(email=valid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)

    assert status == 403


#проверка невалидного мыла
def test_get_api_key_invalid_user(email=invalid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)

    assert status == 403


#проверка невалидного пароля/мыла
def test_get_api_key_for_invalid(email=invalid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)

    assert status == 403


#невалидное имя
def test_add_new_pet_with_invalid_name(name='15131', animal_type='дог', age='5'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 400
    assert result['name'] == name


#без фото
def test_add_new_pet_without_photo(name='Koza', animal_type='kozochka', age='1'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200




def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, "Суперкот", "кот", "3")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status != 200
    assert pet_id not in my_pets.values()

#добавить без обязательного имени
def test_post_add_new_pet_with_invalid_name(name='', animal_type='китя', age='1'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status != 200
    assert result['name'] != name

def test_add_photo_of_pet(pet_photo = 'images/kot.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    if len(my_pets['pets']) >0 and my_pets['pets'][0]['pet_photo'] == '':
        status, result = pf.add_photo_of_pet(auth_key,my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
        assert 'pet_photo' != ''
    else:
        raise Exception('У питомца есть фото')