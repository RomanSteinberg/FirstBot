# -*- coding: utf-8 -*-
from collections import defaultdict
import logging

from telegram.ext import Filters, MessageHandler
from telegram.ext import Updater

from people_bot.storages import HandMadeStorage
from people_bot.handlers import main_handler


class PeopleInfoBot:
    """
    Класс выполняет роль контролллера. Предназначен для настройки и запуска бота.
    """
    def __init__(self, token):
        self.updater = Updater(token=token)  # заводим апдейтера
        handler = MessageHandler(Filters.text | Filters.command, self.handle_message)
        self.updater.dispatcher.add_handler(handler)  # ставим обработчик всех текстовых сообщений
        self.handlers = defaultdict(main_handler)  # id чата -> обработчик генератор
        self.storages = defaultdict(HandMadeStorage)  # id чата -> хранилище
        logging.basicConfig(filename='bot.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)

    def start(self):
        self.updater.start_polling()
        self.updater.idle()

    def handle_message(self, bot, update):
        chat_id = update.message.chat_id
        logging.info(f'chat_id: {chat_id}, received: {update.message}')

        if not chat_id in self.handlers:
            next(self.handlers[chat_id])  # запускаем генератор

        # обработка
        answer = ''
        try:
            answer = self.handlers[chat_id].send((update.message, self.storages[chat_id]))
        except StopIteration:
            # если при этом генератор закончился, начинаем общение с начала
            del self.handlers[chat_id]
            # повторно вызванный, этот метод запустит заново цикл обработки сообщений
            return self.handle_message(bot, update)
        except Exception as e:
            if hasattr(e, 'message'):
                logging.error(e.message)
            else:
                logging.error(e)

        logging.info(f'chat_id: {chat_id}, answer: {answer}')
        bot.sendMessage(chat_id=chat_id, text=answer)
