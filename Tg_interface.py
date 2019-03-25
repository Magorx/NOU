#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import Interface
import time


class TgBot(Interface.Interface):
    def __init__(self, platform, name, bot):
        self.platform = platform
        self.name = name
        self.bot = bot

    def send_msg(self, user, text):
        self.bot.send_message(user.tg_chat_id, text)

    def handle(self, message):
        chat = message.chat
        text = message.text
        user = self.platform.user_by_tg_chat_id(chat.id)
        print('Msg recieved: ' + text)
        
        if user is None:
            self.platform.register_user(message.from_user.username, {'tg_chat_id' : chat.id})

        user = self.platform.user_by_tg_chat_id(chat.id)
        
        self.handle_text(user, text)