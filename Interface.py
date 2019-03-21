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
        #print('[NEW] ' + 'Situation {} created, link = {}'.format(situation.name, situation.link))

        text = 'New situation!\n\n'
        text = text + situation.get_brief_info() + '\n\n'
        text = text + 'Do you want to become pinger in it?'
        self.send_msg(user, text)

    def warn_ping_time(self, user, situation):
        #print('[PNG] Ping time for {} in {}'.format(user.name, situation.name))
        
        text = '/ping time for {}!\n/pong'.format(situation.name)
        self.send_msg(user, text)

    def warn_ping_not_given(self, user, situation):
        #print('[!!!] Ping not given by {} in {}'.format(user.name, situation.name))
        
        text = 'Person is having trouble in {}!'.format(situation.name)
        self.send_msg(user, text)
        self.send_emergency_text(user, situation)

    def warn_emergency_given(self, user, situation):
        #print('[!!!] Emergency given by {} in {}'.format(user.name, situation.name))

        text = 'Emergency was sent for {}!'.format(situation.name)
        self.send_msg(user, text)
        self.send_emergency_text(user, situation)

    def send_emergency_text(self, user, situation):
        #print('[!!!] Emergency text sent by {} in {}'.format(user.name, situation.name))

        if situation.emergency_level >= len(situation.emergency_texts):
            text = 'Maximum emergency for {}!'.format(situation.name)
        else:
            text = situation.emergency_texts[situation.emergency_level]

        self.send_msg(user, text)
