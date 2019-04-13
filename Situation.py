#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

PING = 1
PONG = -1

NOT_STARTED = 10
RUNNING = 11
FINISHED = 12


COMMAND_JOIN = '/joinsit_'
COMMAND_CREATION = '/newsit'
COMMAND_DELETE = '/delsit_'
COMMAND_LIST = '/listsit'


class Situation:
    max_id = 0

    def __init__(self, user, danger_status=1, start_time=0, end_time=0, ping_freq=1, ping_length=0, emergency_texts=[], name='NoName', interface=None, update_max_id=0):
        Situation.max_id += 1
        self.id = Situation.max_id

        self.user = user
        self.danger_status = danger_status
        self.start_time = start_time
        self.end_time = end_time
        self.ping_freq = ping_freq
        self.ping_length = ping_length

        if self.ping_length >= self.ping_freq:
            self.ping_length = self.ping_freq - 1
        
        self.pingers = []
        
        self.emergency_texts = emergency_texts
        self.emergency_level = 0
        
        self.last_ping_check = int(time.time())
        self.last_answer_time = int(time.time()) # some fake sistem answer, used to stop emergency duplications
        self.last_user_answer_time = int(time.time()) # real user answer
        self.last_answer_type = PING 
        
        self.name = name
        self.status = NOT_STARTED
        self.interface = interface
        self.update_link()

        if update_max_id:
            Situation.max_id = update_max_id

    def update_link(self):
        self.link = str(self.id) + '_' + self.name

    def connect_pinger(self, user):
        self.pingers.append(user)

    def disconnect_pinger(self, pinger):
        for i in range(len(self.pingers)):
            if self.pingers[i] == pinger:
                del self.pingers[i]

    def ponged(self):
        t = int(time.time())
        self.last_user_answer_time = t
        self.last_answer_time = t
        self.emergency_level = -1
        
    def check(self):
        cur_time = int(time.time())
        
        if cur_time < self.start_time and not self.status == RUNNING:
            return

        if self.status == FINISHED:
            return

        if cur_time >= self.start_time:
            self.status = RUNNING

        if cur_time >= self.end_time:
            self.status = FINISHED
            return
        
        if cur_time - self.last_ping_check > self.ping_freq:
            self.interface.warn_ping_time(self.user, self)
            self.last_ping_check = cur_time
            self.last_answer_time = cur_time

        if self.last_user_answer_time < self.last_ping_check and cur_time - self.last_answer_time > self.ping_length:
            self.last_answer_time = cur_time
            self.emergency_level += 1
            self.last_answer_time
            self.interface.warn_emergency_given(self.user, self)
            for pinger in self.pingers:
                self.interface.warn_ping_not_given(pinger, self)

    def delete(self):
        for pinger in self.pingers:
            pinger.remove_situation(self)

    def get_brief_info(self):
        return 'Situation[{}] {} by {}:\nemergency level: {}\nstart: {}\nend: {}\nping frequency: {}\nping length: {}'.format(self.id, self.name, self.user.name, self.emergency_level, self.start_time, self.end_time, self.ping_freq, self.ping_length)


def create_emergency_situation(user, interface):
    t = int(time.time())
    sit = Situation(user, 10, t, t + 60, 5, 4, ['This is emergency!'] * 5, interface=interface)
    return sit
