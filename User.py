#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import time
import Situation


class User:
    max_id = -1
    def __init__(self, name, interface_ids_dict):
        User.max_id += 1
        self.id = User.max_id

        self.name = name
        for key in interface_ids_dict:
            self.add_interface(key, interface_ids_dict[key])

        self.situations = []
        self.own_situations = []

        self.creating_situation = 0
        self.new_situation = Situation.Situation(self)


    def add_interface(self, key, value):
        self.__dict__[key] = value

    def join_situation(self, situation):
        if self in situation.pingers:
            return False

        situation.add_pinger(self)
        self.situations.append(situation)

        return True

    def created_situation(self, sit):
        self.own_situations.append(sit)

    def ponged(self):
        print(self.own_situations)
        for sit in self.own_situations:
            if sit.status == Situation.RUNNING:
                print('sit[{}] ponged'.format(sit.name))
                sit.ponged()