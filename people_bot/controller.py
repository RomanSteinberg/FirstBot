# -*- coding: utf-8 -*-
from collections import defaultdict
from functools import partial

from telegram.ext import Filters
from telegram.ext import MessageHandler, CommandHandler
from telegram.ext import Updater

from people_bot.storages import HandMadeStorage


class PeopleInfoBot:
    def __init__(self, token):
        self.updater = Updater(token=token)  # заводим апдейтера
        self.updater.dispatcher.add_handler(CommandHandler('start', self.__start))
        self.updater.dispatcher.add_handler(CommandHandler('save', self.__save))
        self.updater.dispatcher.add_handler(CommandHandler('del', self.__delete))
        self.updater.dispatcher.add_handler(CommandHandler('list', self.__get_list))
        self.storages = defaultdict(HandMadeStorage)  # id чата -> хранилище

    def start(self):
        self.updater.start_polling()
        self.updater.idle()

    def __start(self, bot, update):
        chat_id, storage, message_sender = self.__common_operations(bot, update)
        message_sender(text='Hello! Storage is empty and ready to be filled!')

    def __save(self, bot, update):
        """
        Обработчик команды save.
        Args:
            bot:
            update:

        Returns: None
        """
        chat_id, storage, message_sender = self.__common_operations(bot, update)
        attributes = update.message.split(';')
        self.__act_safely(storage.delete, [attributes], message_sender,
                          'Person info successfully saved!', 'Error! Person info wasn\'t saved!')

    def __delete(self, bot, update):
        chat_id, storage, message_sender = self.__common_operations(bot, update)
        if not update.message.isdigit():
            message_sender('You should provide')
        person_id = int(update.message)
        self.__act_safely(storage.delete, [person_id], message_sender,
                          'Person info was successfully deleted!', 'Error! Person info wasn\'t deleted!')
        # todo: будет не очень корректно не удалять несуществующий объект но при этом сообщать, что удален

    def __get_list(self, bot, update):
        chat_id, storage, message_sender = self.__common_operations(bot, update)
        try:
            info_list = storage.get_list()
            message_sender(text=info_list)
        except Exception:
            message_sender(text='Error! List can\'t be shown!')

    def __common_operations(self, bot, update):
        chat_id = update.message.chat_id
        storage = self.storages[chat_id]
        message_sender = partial(bot.sendMessage, chat_id=chat_id)
        return chat_id, storage, message_sender

    @staticmethod
    def __act_safely(action, args, message_sender, success_msg, fail_message):
        try:
            action(*args)
            message_sender(text=success_msg)
        except Exception:
            message_sender(text=fail_message)
