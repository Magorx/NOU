#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Interface:
    def __init__(self, platform, name):
        self.platform = platform
        self.name = name

    def register(self, user):
        pass # that method must be writen

    def send_msg(self, user, text):
        pass # that method must be writen

    def recive_data(self, user):
        pass # that method must be writen

    def warn_new_situation(self, user, situation):
        text = 'New situation!\n\n'
        text = text + situation.get_brief_info() + '\n\n'
        text = text + 'Do you want to become pinger in it?'
        
        self.send_msg(user, text)

    def warn_ping_time(self, user, situation):
        text = 'Ping time for {}!'.format(self.name)

        self.send_msg(self, user, text)

    def warn_ping_not_given(self, user, situation):
        text = 'Person is having trouble in {}!'.format(self.name)

        self.send_msg(user, text)
        self.send_emergency_text(user, situation)

    def warn_emergency_given(self, user, situation):
        text = 'Emergency was sent for {}!'.format(self.name)

        self.send_msg(user, text)
        self.send_emergency_text(user, situation)

    def send_emergency_text(self, user, situation):
        if situation.emergency_level >= len(situation.emergency_texts):
            text = 'Maximum emergency for {}!'.format(situation.name)
        else:
            text = situation.emergency_texts[situation.emergency_level]

        send.send_msg(user, text)
