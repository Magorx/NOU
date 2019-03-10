#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import time
from random import randint, choice
from time import sleep
import telebot
import re
from os import environ
#from os import environ

#TeleBot = telebot.TeleBot(environ['token'])
TeleBot = telebot.TeleBot(environ['token'])

PING = 1
PONG = -1

NOT_STARTED = 10
RUNNING = 11
FINISHED = 12

USERS = {}
SITUATIONS = {}


class System:
    def __init__(self, name):
        self.situations = []
        self.users = []
        self.systems = []

        self.status = RUNNING

    def register_user(self, user):
        for sit in user.situations:
            if sit.status != FINISHED:
                self.situations.append(sit)
                for usr in self.users:
                    usr.warn_new_situation(sit)

        self.users.append(user)


class Situation:
    max_id = -1

    def __init__(self, user, danger_status, start_time, end_time, ping_freq, ping_length, emergency_texts=[], name='NoName'):
        self.user = user
        self.danger_status = danger_status
        self.start_time = start_time
        self.end_time = end_time
        self.ping_freq = ping_freq
        self.ping_length = ping_length
        
        self.pingers = []
        
        self.emergency_texts = emergency_texts
        self.emergency_level = 0
        
        self.last_ping_check = int(time.time())
        self.last_answer_time = int(time.time())
        self.last_user_answer_time = int(time.time())
        self.last_answer_type = PING
        
        self.name = name
        self.status = RUNNING
        
    def check(self):
        cur_time = int(time.time())
        
        if cur_time < self.start_time:
            return

        if self.status == FINISHED:
            return

        if cur_time >= end_time:
            self.status = FINISHED
            return
        
        if cur_time - self.last_ping_check > self.ping_freq:
            user.warn_ping(self)
            self.last_ping_check = cur_time
        
        if self.last_answer_time < self.last_ping_check and cur_time - self.last_ping_check > self.ping_length:
            self.emergency_level += 1
            self.last_answer_time
            self.user.warn_emergency(self)
            for pinger in self.pingers:
                pinger.warn_ping_not_given(self)

    def get_brief_info(self):
        return 'Situation[{}] {} by {}:\nemergency level: {}\nstart: {}\nend: {}\nping frequency: {}\nping length: {}'.format(self.id, self.name, self.user.name, self.emergency_level, self.start_time, self.end_time, self.ping_freq, self.ping_length)


class User:
    max_id = -1
    def __init__(self, chat_id, tg_login):
        User.max_id += 1
        self.id = User.max_id
        self.chat_id = chat_id
        self.tg_login = login
        
        self.situations = []
        self.friends = []
        self.pingers = []
        self.extreme_pingers = []

        self.systems = []

    def warn_new_situation(self, situation):
        text = 'New situation!\n\n'
        text = text + situation.get_brief_info() + '\n\n'
        text = text + 'Do you want to become pinger in it?'
        TeleBot.send_message(self.chat_id, text)

    def warn_ping(self, situation):
        TeleBot.send_message(self.chat_id, 'Ping time for {}!'.format(self.name))

    def warn_ping_not_given(self, situation):
        TeleBot.send_message(self.chat_id, 'Person is having trouble in {}!'.format(self.name))
        self.send_emergency_text(situation)

    def warn_emergency(self, situation):
        TeleBot.send_message(self.user.chat_id, 'Emergency was sent for {}!'.format(self.name))
        self.send_emergency_text(situation)

    def send_emergency_text(self, situation):
        if self.emergency_level >= len(self.emergency_texts):
            TeleBot.send_message(pinger.chat_id, 'Maximum emergency for {}!'.format(situation.name))
        else:
            TeleBot.send_message(pinger.chat_id, situation.emergency_texts[situation.emergency_level])


def user_by_id(user_id):
    if user_id in USERS:
        return USERS[user_id]
    else:
        return None

def warn_invalid_args(chat_id):
    TeleBot.send_message(chat_id, 'Некоректные аргументы')


@TeleBot.message_handler(func=lambda x: True)
def message_handler(message):
    for sit in SITUATIONS:
        sit.check()

    if TO_STOP:
        print('ok')
        exit(0)

    chat = message.chat
    text = message.text
    user = user_by_id(chat.id)
    print('Got message from {}: {}'.format(chat.first_name, text))
    if user is None and text != '/start':
        TeleBot.send_message(chat.id, 'Напишите мне, пожалуйста, /start, ' +
                             'чтобы я добавил вас в список пользователей')
        return 0

    if text == '/start':
        TeleBot.send_message(chat.id, 'Привет. Правила доступны по /rules, ' +
                                      'помощь - по /commands_help')
        USERS[chat.id] = User(chat.id, chat.first_name)

    # /new_situation_NOU_10_60_1_1_help!\nresqueme!\n
    if text.startswith('/new_situation'):
        args = text[13:].split('_')
        try:
            name = args[0]
            danger = int(args[1])
            sit_len = int(args[2])
            freq = int(args[3])
            length = int(args[4])
            texts = args[5].split('\\n')
            stat_time = int(time.time())
            end_time = start_time + sit_len * 60
            sit = Situation(user, danger, start_time, end_time, freq, length, texts, name)
            
            SITUATIONS.append(sit)
            TeleBot.send_message(user.id, 'Ситуация создана!')
        except Exception:
            warn_invalid_args(user.id)


def main():
    global USERS
    USERS = {}
    while True:
        msg = input()
    TeleBot.polling(interval=1)


if __name__ == "__main__":
    main()
    
    
            
    