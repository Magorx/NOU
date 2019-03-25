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

        self.sistems = []
        # todo - importing sistems from databse        

    def add_interface(self, key, interface):
        self.interfaces[key] = interface

    def register_user(self, name, interface_ids_dict):
        user = User.User(name, interface_ids_dict)
        self.users.append(user)

    def add_situation(self, situation):
        self.situations.append(situation)
        situation.user.created_situation(situation)

    def add_sistem(self, sistem):
        self.sistems.append(sistem)

    def remove_situation(self, situation):
        for i in range(len(self.situations)):
            sit = self.situations[i]
            if sit == situation:
                sit.delete()
                del self.situations[i]
    
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

    def sistem_by_id(self, id):
        for sis in self.sistems:
            if sis.id == id:
                return sis
        return None

    def check_situations(self):
        for sit in self.situations:
            sit.check()

    def text_dump(self):
        print(self.situations)
        print(self.users)
