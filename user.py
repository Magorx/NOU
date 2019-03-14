#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class User:
    max_id = -1
    def __init__(self, name, interface_ids_dict):
        User.max_id += 1
        self.id = User.max_id

        self.name = name

        for key in interface_ids_dict:
            self.__dict__[key] = interface_ids_dict[key]
