#!/usr/bin/env python3
# -*- coding: utf-8 -*-


COMMAND_JOIN = '/joinsis_'
COMMAND_CREATION = '/newsis'
COMMAND_DELETE = '/delsis_'


class Sistem:
    max_id = -1
    def __init__(self, creator, max_user_count=0, name='NoName'):
        Sistem.max_id += 1
        self.id = Sistem.max_id

        self.name = name
        self.creator = creator

        self.situations = []
        self.users = []
        self.sistems = []

        self.max_user_count = max_user_count
        self.update_link()

    def update_link(self):
        self.link = str(self.id) + '_' + self.name

    def add_user(self, user):
        if len(self.users) >= self.max_user_count:
            return False
        else:
            self.users.append(user)
            return True

    def add_situation(self, situation):
        sit = situation
        if sit in self.situations:
            return

        self.situations.append(sit)

        for usr in self.users:
            if not self in usr.muted:
                usr.warn_new_situation(usr, sit)

    def add_sistem(self, sistem):
        self.sistem.append(sistem)
