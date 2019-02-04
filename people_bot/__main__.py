# -*- coding: utf-8 -*-

import yaml
from os import path
from people_bot.controller import PeopleInfoBot


def main():
    cfg_path = 'config.yaml'
    if not path.exists(cfg_path):
        print('Скопируйте файл default-config.yaml, переименуйте его в config.yaml, укажите параматеры.')
        return
    config = yaml.load(open('config.yaml'))
    bot = PeopleInfoBot(config['token'])
    bot.start()


if __name__ == '__main__':
    main()
