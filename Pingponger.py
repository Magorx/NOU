#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import User
import Situation


class Pingponger:
    def __init__(self, a_number, interfaces={}, users_database=None, situations_database=None):
        self.a_number = a_number
        self.interfaces = interfaces
        
        self.users = []
        # todo - importing users from databse

        self.situations = []
        # todo - importing situations from databse

    def add_interface(self, key, interface):
        self.interfaces[key] = interface

    def register_user(self, name, interface_ids_dict):
        user = User.User(name, interface_ids_dict)
        self.users.append(user)

    def add_situation(self, situation):
        self.situations.append(situation)
    
    def init_situation_creation(self, user):
        pass

    def user_by_tg_chat_id(self, chat_id):
        for user in self.users:
            if user.tg_chat_id == chat_id:
                return user
        return None

    def situation_by_id(self, id):
        for sit in self.situations:
            if sit.id == id and sit.status != Situation.FINISHED:
                return sit
        return None

    def handle_message(self, message):
        pass

    def text_dump(self):
        print(self.situations)
        print(self.users)
