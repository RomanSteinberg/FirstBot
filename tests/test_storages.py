import unittest
from people_bot import HandMadeStorage, BotStorage


class CorrectStorage(BotStorage):
    """
    Класс компактно реализует хранилище, но функция get_lists работает медленно. Класс нужен для тестирования.
    """
    def __init__(self):
        super(CorrectStorage, self).__init__()
        self._people = dict()

    def add(self, person: list):
        self._people[person[0]] = {attr: value for attr, value in zip(self._attributes, person[1:])}

    def delete(self, person_id: int):
        if person_id in self._people:
            del self._people[person_id]

    def get_list(self):
        result = ''
        for pid, info in sorted(self._people.items()):
            str_info = ' | '.join(str(value) for attr, value in info.items())
            result += f'{pid}: {str_info}\n'
        return result


class TestStorageMethods(unittest.TestCase):
    """
    Тестируем реализацию хранилищ.
    """
    def setUp(self):
        self.hm_storage = HandMadeStorage()
        self.c_storage = CorrectStorage()

    def __add(self, person: list):
        self.hm_storage.add(person)
        self.c_storage.add(person)

    def __del(self, person_id: int):
        self.hm_storage.delete(person_id)
        self.c_storage.delete(person_id)

    def __compare_states(self):
        obtained = self.hm_storage.get_list()
        expected = self.c_storage.get_list()
        self.assertEqual(obtained, expected)

    def test_add(self):
        parsed_record = [1, 'Иван Иванович Иванов', 20, 'м', 'Карфаген', 'Карфаген']
        self.__add(parsed_record)

        self.__compare_states()

    def test_misses(self):
        # удаление несуществующего
        self.__del(1)
        self.__compare_states()

        # повторное добавление
        parsed_record = [1, 'Иван Иванович Иванов', 20, 'м', 'Карфаген', 'Карфаген']
        self.__add(parsed_record)
        self.__add(parsed_record)
        self.__compare_states()

    def test_add_and_del(self):
        parsed_record = [1, 'Иван Иванович Иванов', 20, 'м', 'Карфаген', 'Карфаген']
        self.__add(parsed_record)
        # добавим еще
        parsed_record[0] = 2
        self.__add(parsed_record)
        # удалим
        self.__del(1)

        self.__compare_states()

    def test_multiple_add(self):
        parsed_record = [1, 'Иван Иванович Иванов', 20, 'м', 'Карфаген', 'Карфаген']
        for pid in [4, 7, 5, 9, 8, 2, 1, 10, 12]:
            parsed_record[0] = pid
            self.__add(parsed_record)

        self.__compare_states()

    def test_multiple_operations(self):
        parsed_record = [1, 'Иван Иванович Иванов', 20, 'м', 'Карфаген', 'Карфаген']
        for pid, action in [(4, 'add'), (7, 'add'), (5, 'add'), (7, 'del'), (9, 'add'), (8, 'add'), (4, 'del')]:
            if action == 'add':
                parsed_record[0] = pid
                self.__add(parsed_record)
            elif action == 'del':
                self.__del(pid)

        self.__compare_states()


if __name__ == '__main__':
    unittest.main()
