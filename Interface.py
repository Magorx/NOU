#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import Situation
import Sistem


class Interface:
    def __init__(self, platform, name):
        self.platform = platform
        self.name = name

    def register(self, user):
        pass # that method must be writen

    def send_msg(self, user, text):
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

    def handle_text(self, user, text):
        if user.creating_situation:
            if text == '/cancel':
                self.send_msg(user, 'Создание ситуации отменено')
                user.creating_situation = 0
            
            try:
                stage = user.creating_situation
                new_sit = user.new_situation
                if stage == 1:
                    new_sit.name = text
                    new_sit.update_link()
                    self.send_msg(user, 'Введите степень опасности (от 1 до 10)')
                    user.creating_situation += 1
                elif stage == 2:
                    new_sit.danger_status = int(text)
                    self.send_msg(user, 'Введите время до ситуации в формате hh:mm')
                    user.creating_situation += 1
                elif stage == 3:
                    h, m = map(int, text.split(':'))
                    m += h * 60
                    s = m * 60
                    new_sit.start_time = int(time.time() + s)
                    self.send_msg(user, 'Введите длительность ситуации в формате hh:mm')
                    user.creating_situation += 1
                elif stage == 4:
                    h, m = map(int, text.split(':'))
                    m += h * 60
                    s = m * 60
                    new_sit.end_time = new_sit.start_time + int(time.time() + s)
                    self.send_msg(user, 'Введите частоту проверок в формате mm:ss')
                    user.creating_situation += 1
                elif stage == 5:
                    m, s = map(int, text.split(':'))
                    s += m * 60
                    new_sit.ping_freq = s
                    self.send_msg(user, 'Введите продолжительность одной проверки в формате mm:ss')
                    user.creating_situation += 1
                elif stage == 6:
                    m, s = map(int, text.split(':'))
                    s += m * 60
                    new_sit.ping_length = s
                    self.send_msg(user, 'Введите экстренные тексты, разделяя их переводом строки')
                    user.creating_situation += 1
                elif stage == 7:
                    new_sit.emergency_texts = text.split('\n')
                    self.send_msg(user, 'Проверьте все введенные данные. Подтверждаете создание ситуации? (Ответьте "Да" без кавычек)')
                    user.creating_situation += 1
                elif stage == 8:
                    if text.lower() == 'да':
                        new_sit.interface = self
                        self.platform.add_situation(new_sit)
                        new_sit.update_link()
                        answer = 'Ситуация создана. Ссылка на присоединение:\n{}{}'.format(Situation.COMMAND_JOIN, new_sit.link)
                    else:
                        answer = 'Создание ситуации отменено'
                    self.send_msg(user, answer)
                    user.new_situation = Situation.Situation(user)
                    user.creating_situation = 0
            except Exception as e:
                self.send_msg(user, 'Неверно введены данные, повторите попытку')
                print(e, '| in creating Situation, text = ' + text)

        elif user.creating_sistem:
            if text == '/cancel':
                self.send_msg(user, 'Создание системы отменено')
                user.creating_situation = 0
            
            try:
                stage = user.creating_sistem
                new_sis = user.new_sistem
                if stage == 1:
                    new_sis.name = text
                    user.creating_sistem += 1
                    self.send_msg(user, 'Введите максимальное число пользователей в системе')
                if stage == 2:
                    new_sis.max_user_count = int(text)
                    user.creating_sistem += 1
                    self.send_msg(user, 'Проверьте все введенные данные. Подтверждаете создание ситуации? (Ответьте "Да" без кавычек)')
                if stage == 3:
                    if text.lower() == 'да':
                        self.platform.add_sistem(new_sis)
                        new_sis.update_link()
                        answer = 'Система создана. Ссылка на присоединение:\n{}{}'.format(Sistem.COMMAND_JOIN, new_sis.link)
                    else:
                        answer = 'Создание системы отменено'
                    self.send_msg(user, answer)
                    user.new_sistem = Sistem.Sistem(user)
                    user.creating_sistem = 0

            except Exception as e:
                self.send_msg(user, 'Неверно введены данные, повторите попытку')
                print(e, '| in creating Sistem, text = ' + text)

        else:
            if text == '/start':
                self.send_msg(user, 'Добро пожаловать в Pingponger!')

            elif text == Situation.COMMAND_CREATION:
                user.creating_situation = 1
                self.send_msg(user, 'Начинаем создание новой ситуации')
                self.send_msg(user, 'Введите название ситуации')

            elif text == Sistem.COMMAND_CREATION:
                user.creating_sistem = 1
                self.send_msg(user, 'Начинаем создание новой системы')
                self.send_msg(user, 'Введите название системы')

            elif text.startswith(Situation.COMMAND_JOIN):
                link = text[len(Situation.COMMAND_JOIN):]
                id = int(link.split('_')[0])

                sit = self.platform.situation_by_id(id)
                if sit is None:
                    self.send_msg(user, 'Несуществующая или окончившаяся ситуация')
                else:
                    ret = user.connect_situation(sit)
                    if ret:
                        self.send_msg(user, 'Вы успешно подключились к ситуации ' + sit.name)
                    else:
                        self.send_msg(user, 'Вы уже подключены к ситуации ' + sit.name)

            elif text.startswith(Sistem.COMMAND_JOIN):
                link = text[len(Situation.COMMAND_JOIN):]
                id = int(link.split('_')[0])

                sis = self.platform.sistem_by_id(id)
                if sis is None:
                    self.send_msg(user, 'Несуществующая система')
                else:
                    ret = sis.add_user(user)
                    if ret:
                        self.send_msg(user, 'Вы удачно подключились к системе {}'.format(sis.name))
                    else:
                        self.send_msg(user, 'В системе достигнуто максимальное количество пользователей')

            elif text.startswith(Situation.COMMAND_DELETE):
                link = text[len(Situation.COMMAND_DELETE):]
                id = int(link.split('_')[0])

                sit = self.platform.situation_by_id(id)
                if sit is None:
                    self.send_msg(user, 'Несуществующая система')
                else:
                    self.platform.remove_situation(sit)
                    self.send_msg(user, 'Ситуация {} удалена'.format(sit.name))
            
            elif text == '/extra':
                sit = Situation.create_emergency_situation(user, self)
                self.platform.add_situation(sit)
                self.send_msg(user, sit.get_brief_info())
                self.send_msg(user, Situation.COMMAND_JOIN + sit.link)

            elif text == '/pong':
                user.ponged()
