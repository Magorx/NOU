#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

PING = 1
PONG = -1

NOT_STARTED = 10
RUNNING = 11
FINISHED = 12


class Situation:
    max_id = -1

    def __init__(self, user, danger_status=1, start_time=0, end_time=0, ping_freq=1, ping_length=0, emergency_texts=[], name='NoName'):
        Situation.max_id += 1
        self.id = Situation.max_id

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
        self.status = NOT_STARTED
        self.update_link()

    def update_link(self):
        self.link = str(self.id) + '_' + self.name

    def add_pinger(self, user):
        self.pingers.append(user)
        
    def check(self):
        TeleBot.send_message(chat.id, 'check started')
        cur_time = int(time.time())
        
        if cur_time < self.start_time and not self.status == RUNNING:
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