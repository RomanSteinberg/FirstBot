# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class BotStorage(ABC):
    """
    Абстрактный класс для хранения данных. Реализует интерфейс add, delete, get_list.
    """
    def __init__(self):
        self._people = dict()
        self._attributes = ['ФИО', 'Возраст', 'Пол', 'Город', 'Страна']

    @abstractmethod
    def add(self, person: list):
        pass

    @abstractmethod
    def delete(self, person_id: int):
        pass

    @abstractmethod
    def get_list(self):
        return ''


class HandMadeStorage(BotStorage):
    """
    Класс реализует хранилище на базе отсортированного списка без использования стандартных функций сортировки
    и удаления.
    """
    def __init__(self):
        super(HandMadeStorage, self).__init__()
        self._people = []  # будем хранить пары (pid, info)

    def add(self, info):
        """
        Добавляет информацию о пользователе. Использует поиск за O(log(N)) в отсортированном списке.
        Args:
            info (list): Информация о пользователе в виде списка из 6 атрибутов. Информация сохраняется как есть
            без валидации.

        Returns (bool):
            True - пользователь добавлен, False - пользователя с таким id уже существует.
        """
        pid = info[0]
        info = {attr: value for attr, value in zip(self._attributes, info[1:])}

        ind = self.__binary_search(pid)
        if len(self._people) == ind or pid != self._people[ind][0]:
            self._people.insert(ind, (pid, info))
            return True
        return False

    def delete(self, person_id):
        """
        Удаляет информацию о пользователе по его идентификатору. Использует поиск за O(log(N)) в отсортированном списке.
        Args:
            person_id (int): Идентификатор пользователя.

        Returns (bool):
            True - пользователь удален, False - пользователя с таким id нет в хранилище.
        """
        ind = self.__binary_search(person_id)
        if 0 <= ind < len(self._people) and person_id == self._people[ind][0]:
            self._people.pop(ind)
            return True
        return False

    def get_list(self):
        """
        Возвращает отсортированный список пользователей.
        Returns(str):
            Строку, состоящую из информации о пользователях, при этом информация о каждом отдельном пользователе
            отделена символом конца строки \n.
        """
        # список хранится отсортированным, значит сразу конвертируем в строку
        result = ''
        for pid, info in self._people:
            str_info = ' | '.join(str(value) for attr, value in info.items())
            result += f'{pid}: {str_info}\n'
        return result

    def __binary_search(self, person_id):
        """
        Бинарный поиск в отсортированном списке.
        Args:
            person_id (int): Идентификатор пользователя.

        Returns (int):
            Позицию элемента с наибольшим id среди тех, id которых меньше либо равны person_id.
        """
        l, r = 0, len(self._people)
        m = l + (r - l) // 2
        while l < r:
            if self._people[m][0] < person_id:
                l = m + 1
            else:
                r = m
            m = l + (r - l) // 2
        return m
