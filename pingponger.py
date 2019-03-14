#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Pingponger:
    def __init__(self, a_number, interfaces=[], users_database=None, situations_database=None):
        self.a_number = a_number
        self.interfaces = interfaces
        
        self.users = []
        # todo - importing users from databse

        self.situations = []
        # todo - importing situations from databse
    
    def init_situation_creation(self, user):
        pass