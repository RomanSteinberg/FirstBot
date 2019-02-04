# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from queue import PriorityQueue


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
    Класс реализует хранилище без использования стандартных функций сортировки и удаления.
    """
    def __init__(self):
        super(HandMadeStorage, self).__init__()
        self._people = []  # будем хранить пары (pid, info)

    def add(self, person: list):
        pid = person[0]
        info = {attr: value for attr, value in zip(self._attributes, person[1:])}

        # реализуем вставку за O(log(N)) в отсортированный списке
        ind = self.__binary_search(pid)
        if len(self._people) == ind or pid != self._people[ind][0]:
            self._people.insert(ind, (pid, info))

    def delete(self, person_id: int):
        # реализуем поиск за O(log(N)) в отсортированном списке
        ind = self.__binary_search(person_id)
        if len(self._people)>0 and person_id == self._people[ind][0]:
            self._people.pop(ind)

    def get_list(self):
        # сортировка вставками уже отработала во время добавления информации, остается только выдать список
        result = ''
        for pid, info in self._people:
            str_info = ' | '.join(str(value) for attr, value in info.items())
            result += f'{pid}: {str_info}\n'
        return result

    def __binary_search(self, pid):
        l, r = 0, len(self._people)
        m = l + (r - l) // 2
        while l < r:
            if self._people[m][0] < pid:
                l = m + 1
            else:
                r = m
            m = l + (r - l) // 2
        return m
