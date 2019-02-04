# -*- coding: utf-8 -*-
# Идея обработчиков на генераторах взята из статьи: https://habr.com/ru/post/316666/
from functools import partial


def main_handler():
    init = yield None
    message, storage = init
    handlers = {'/save': save, '/del': delete, '/list': partial(get_list, storage)}
    h = handlers.get(message.text, unexpected_text)
    yield from h()
    del h


def save():
    message, storage = yield 'Укажите информацию о человеке в следующем формате: \"id;ФИО;пол;возраст;город;страна\".'

    # валидация и разбор
    while True:
        error_message, attributes = parse_info(message.text)
        if len(error_message) == 0:
            break
        message, storage = yield error_message

    # сохранение
    if storage.add(attributes):
        yield 'Информация о человеке успешно сохранена!'
    else:
        yield 'Пользователь с таким id уже существует в хранилище. Сохранение отменено.'


def delete():
    message, storage = yield 'Укажите идентификатор (id) человека.'

    # валидация и разбор
    while not message.text.isdigit():
        message, storage = yield 'Идентификатор должен быть числом'
    person_id = int(message.text)

    # сохранение
    if storage.delete(person_id):
        yield 'Информация о человеке успешно удалена!'
    else:
        yield 'Пользователя с таким id не существует в хранилище. Удаление отменено.'


def get_list(storage):
    res = storage.get_list()
    yield res if len(res) > 0 else 'Ни один человек не внесен в базу.'


def unexpected_text():
    yield 'Введите команды /save, /del или /list.'


def parse_info(info):
    """
    Функция осуществляет разбор текста на 6 составляющих (атрибутов), при этом осуществляется валидация
    введенной информации.
    Args:
        info: Текст сообщения пользователя, который нужно разобрать.

    Returns (tuple):
        Пару, которая состоит из сообщения об ошибке и списка атрибутов. Если при валидации ошибок не было, то
        сообщение будет пустой строкой, а атрибуты будут приведены к стандартному виду.
    """
    attributes = info.split(';')
    # количество аттрибутов
    if len(attributes) != 6:
        return 'Информация о человеке представляет собой 6 атрибутов, разделенных символом \";\". ' \
               'Формат: \"id;ФИО;пол;возраст;город;страна\".', attributes

    # id
    if attributes[0].isdigit():
        attributes[0] = int(attributes[0])
    else:
        return 'Идентификатор должен быть числом', attributes

    # возраст
    if attributes[2].isdigit():
        attributes[2] = int(attributes[2])
    else:
        return 'Возраст должен быть числом', attributes

    # пол
    attributes[3] = attributes[3].lower()
    if attributes[3] not in ['м', 'ж', 'муж', 'жен']:
        return 'Пол может быть одним из следующих значений: м, ж, муж, жен.', attributes

    # ФИО, город и страна
    for i in [1, 4, 5]:
        attributes[i] = attributes[i].capitalize()

    return '', attributes
