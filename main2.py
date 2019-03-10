#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from random import randint, choice
from time import sleep
import telebot
from os import environ


TeleBot = telebot.TeleBot(environ['token'])
ADMIN_ID = [150486866]

TO_STOP = False


class Tyle(object):
    def __init__(self, x, y, bonus, owner=None):
        self.x = x
        self.y = y
        self.bonus = bonus
        self.owner = owner

        self.last_round_bonus = 0
        self.score = 0
        self.bets = {}

        self.update()

    def update(self):
        if self.owner is None:
            self.symb = str(self.bonus)
        else:
            self.symb = self.owner.name[0]

    def bet(self, player, count):
        if player.points < count:
            return 'Недостаточно очков для ставки.'
        if player in self.bets:
            self.bets[player] += count
        else:
            self.bets[player] = count
        player.points -= count
        self.score += count
        return 'Ставка засчитана. Осталось {} очков.'.format(player.points)

    def find_winners(self):
        winners = []
        winning_score = 0
        bets = self.bets
        for player in bets:
            if bets[player] > winning_score:
                winners = [player]
                winning_score = bets[player]
            elif bets[player] == winning_score:
                winners.append(player)
        return winners, winning_score

    def capture(self):
        full_score = self.score + self.bonus
        bets = self.bets
        winners, winning_score = self.find_winners()
        self.last_round_bonus = self.bonus

        if len(winners) == 0:
            pass
        elif len(winners) == 1:
            winner = winners[0]
            self.owner = winner
            winner.score += full_score
            winner.last_round_score += full_score
        elif len(winners) > 1:
            self.bonus = full_score

        self.score = 0
        self.update()
        return winners, winning_score, bets, full_score

    def dump(self):
        print('Tyle[{}][{}] Score[{}] Bets: {}'.format(self.x, self.y, 
                                                       self.score, self.bets))


class World(object):
    def __init__(self, id, width, height, start_points, admin, min_players, 
                 max_players):
        self.id = id
        self.map = [[Tyle(j, i, choices([_ for _ in range(4)], [1, 4, 3, 2]) + 2) 
                                for i in range(height)] for j in range(width)]
        self.map[randint(0, width - 1)][randint(0, height - 1)].bonus = 7
        self.width = width
        self.height = height
        self.start_points = start_points
        self.admin = admin
        self.min_players = min_players
        self.max_players = max_players

        self.players = []
        self.results = None
        self.running = False
        self.round = 0

    def add_player(self, player):
        if player not in self.players:
            self.players.append(player)
            player.world = self
            if len(self.players) >= self.min_players:
                self.running = True
            return 'Вы успешно присоединились к миру.'
        elif player.world is not self:
            player.World = self
            return 'Вы успешно присоединились к миру.'
        else:
            return 'Вы уже присоединены к этому миру.'

    def new_round(self):
        self.round += 1
        width = self.width
        height = self.height
        self.map = [[Tyle(j, i, choices([_ for _ in range(4)], [1, 4, 3, 2]) + 2) 
                                for i in range(height)] for j in range(width)]
        self.map[randint(0, width - 1)][randint(0, height - 1)].bonus = 5
        for player in self.players:
            player.points = self.start_points
        self.results = None

    def bet(self, player, x, y, count):
        if player not in self.players:
            return 'Something went wrong'
        if player.points < count:
            return 'Недостаточно очков для ставки.'
        return self.map[x][y].bet(player, count)

    def full_capture(self):
        world_map = self.map
        results = []
        for x in range(self.width):
            for y in range(self.height):
                tyle = world_map[x][y]
                winners, winning_score, bets, score = tyle.capture()
                if winners is None:
                    pass
                elif len(winners) >= 1:
                    results.append((tyle, winners, winning_score, bets, score))
                    tyle.bets = {}
        round_max_score = -1
        round_winner = None
        for player in self.players:
            if player.score > round_max_score:
                round_winner = player
                round_max_score = player.score
            player.last_round_score = player.score
            player.score = 0

        self.results = results
        self.round_winner = round_winner
        self.round_max_score = round_max_score
        return results, (round_winner, round_max_score)

    def get_formated_results(self):
        results = self.results
        to_return = ''
        for res in results:
            tyle = res[0]
            winners = res[1]
            winning_score = res[2]
            bets = res[3]
            score = res[4]

            to_return = to_return + 'Клетка [{}][{}] (бонус {}):\n'.format(
                tyle.x + 1, tyle.y + 1, tyle.last_round_bonus)
            for player in bets:
                to_return = to_return + '  {} - {}\n'.format(bets[player], 
                                                             player)
            to_return = to_return + '--------------\n'
            to_return = to_return + '{} '.format(score)
            if len(winners) == 1:
                to_return = to_return + '-> {}\n\n'.format(winners[0])
            else:
                to_return = to_return + 'уходят в бонус, ничья.\n\n'
        to_return = to_return + '\n'
        for player in self.players:
            to_return = to_return + '{}: {} очков\n'.format(
                player.name, player.last_round_score)
        to_return = to_return + '-----\n'
        to_return = to_return + 'Победитель: {}. Очки: {}\n'.format(
            self.round_winner, self.round_max_score)

        return to_return

    def get_to_show(self):
        to_return = ''
        for x in range(self.height):
            for y in range(self.width):
                self.map[y][x].update()
                to_return = to_return + self.map[y][x].symb + ' '
            to_return = to_return + '\n'
        return to_return


class Player(object):
    def __init__(self, user, name, world_id=None):
        self.user = user
        self.name = name

        self.points = WORLDS[world_id].start_points
        self.score = 0
        self.last_round_score = 0
        if world_id:
            self.join_world(world_id)

    def __repr__(self):
        return str(self.name)

    def join_world(self, world_id):
        if world_id in WORLDS:
            return WORLDS[world_id].add_player(self)
        else:
            return 'Мира с таким названием не существует.'

    def bet(self, x, y, count):
        if self.world is None:
            return 'Вы не участвуете в игре'
        else:
            return self.world.bet(self, x, y, count)


def choices(population, weights=None, k=1):
    if weights is None:
        randomizing_arr = population
    elif len(weights) != len(population):
        raise IndexError
    else:
        randomizing_arr = []
        for i in range(len(population)):
            for j in range(weights[i]):
                randomizing_arr.append(population[i])

    result_arr = []
    for i in range(k):
        result_arr.append(choice(randomizing_arr))

    if len(result_arr) == 1:
        return result_arr[0]
    else:
        return result_arr


#===== TELEGRAMM INTERFACE ===================================================
class User(object):
    def __init__(self, telegramm_id, name):
        self.id = telegramm_id
        self.name = name
        self.worlds = []
        self.players = []
        self.victory_count = 0

    def join_world(self, world_id):
        if world_id not in WORLDS:
            return 'Мира с таким названием не существует.'
        if WORLDS[world_id] in self.worlds:
            return 'Вы уже присоединены к этому миру.'

        world = WORLDS[world_id]
        new_player = Player(self, self.name, world.id)
        self.worlds.append(world)
        self.players.append(new_player)
        return 'Вы успешно присоединились к миру.'


def user_by_id(user_id):
    if user_id in USERS:
        return USERS[user_id]
    else:
        return None


def world_by_id(world_id):
    if world_id in WORLDS:
        return WORLDS[world_id]
    else:
        return None


def player_by_world(user, world):
    if world in user.worlds:
        return user.players[user.worlds.index(world)]
    else:
        return None


def send_to_all_in_world(world, message):
    if world is None or not message:
        return 0

    for player in world.players:
        TeleBot.send_message(player.user.id, message)


def warn_invalid_args(chat_id):
    TeleBot.send_message(chat_id, 'Некоректные аргументы. ' + 
                                  '/commands_help для помощи.')


def warn_world_not_exist(chat_id):
    TeleBot.send_message(chat_id, 'Такого мира не существует.')


def warn_invalid_coords(chat_id):
    TeleBot.send_message(chat_id, 'Введенные координаты не подходят.')


def warn_invalid_points(chat_id):
    TeleBot.send_message(chat_id, 'Операция с таким количеством очков не ' +
                                  'возможна')


def warn_invalid_sizes(chat_id):
    TeleBot.send_message(chat_id, 'Операция не возможна с данными размерами.')


def warn_player_not_in_world(chat_id):
    TeleBot.send_message(chat_id, 'Вы не участвуете в этом мире.')


def warn_player_not_admin(chat_id):
    TeleBot.send_message(chat_id, 'Вы не админ в этом мире.')


def warn_world_not_running_not_enough_players(chat_id):
    TeleBot.send_message(chat_id, 'Этот мир еще не запущен, надо больше ' +
                                  'игроков.')


@TeleBot.message_handler(commands=['stop'])
def command_start(message):
    if message.chat.id in ADMIN_ID:
        TeleBot.send_message(message.chat.id, 'Остановлен.')
        print('Killed by {}'.format(message.chat.first_name))
        global TO_STOP
        TO_STOP = True


@TeleBot.message_handler(commands=['rules'])
def command_rules(message):
    chat = message.chat
    TeleBot.send_message(chat.id, open('rules.txt', 'r').read())

@TeleBot.message_handler(commands=['commands_help'])
def command_rules(message):
    chat = message.chat
    TeleBot.send_message(chat.id, open('commands_help.txt', 'r').read())

PING = 1
PONG = -1

NOT_STARTED = 10
RUNNING = 11
FINISHED = 12

USERS = {}
SITUATIONS = {}


class System:
    def __init__(self, name):
        self.situations = []
        self.users = []
        self.systems = []

        self.status = RUNNING

    def register_user(self, user):
        for sit in user.situations:
            if sit.status != FINISHED:
                self.situations.append(sit)
                for usr in self.users:
                    usr.warn_new_situation(sit)

        self.users.append(user)


class Situation:
    max_id = -1

    def __init__(self, user, danger_status, start_time, end_time, ping_freq, ping_length, emergency_texts=[], name='NoName'):
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
        self.status = RUNNING
        
    def check(self):
        cur_time = int(time.time())
        
        if cur_time < self.start_time:
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


class User:
    max_id = -1
    def __init__(self, chat_id, tg_login):
        User.max_id += 1
        self.id = User.max_id
        self.chat_id = chat_id
        self.tg_login = login
        
        self.situations = []
        self.friends = []
        self.pingers = []
        self.extreme_pingers = []

        self.systems = []

    def warn_new_situation(self, situation):
        text = 'New situation!\n\n'
        text = text + situation.get_brief_info() + '\n\n'
        text = text + 'Do you want to become pinger in it?'
        TeleBot.send_message(self.chat_id, text)

    def warn_ping(self, situation):
        TeleBot.send_message(self.chat_id, 'Ping time for {}!'.format(self.name))

    def warn_ping_not_given(self, situation):
        TeleBot.send_message(self.chat_id, 'Person is having trouble in {}!'.format(self.name))
        self.send_emergency_text(situation)

    def warn_emergency(self, situation):
        TeleBot.send_message(self.user.chat_id, 'Emergency was sent for {}!'.format(self.name))
        self.send_emergency_text(situation)

    def send_emergency_text(self, situation):
        if self.emergency_level >= len(self.emergency_texts):
            TeleBot.send_message(pinger.chat_id, 'Maximum emergency for {}!'.format(situation.name))
        else:
            TeleBot.send_message(pinger.chat_id, situation.emergency_texts[situation.emergency_level])


@TeleBot.message_handler(func=lambda x: True)
def message_handler(message):
    if TO_STOP:
        print('ok')
        exit(0)

    chat = message.chat
    text = message.text
    user = user_by_id(chat.id)
    TeleBot.send_message(chat.id, text)
    print('Got message from {}: {}'.format(chat.first_name, text))
    if user is None and text != '/start':
        TeleBot.send_message(chat.id, 'Напишите мне, пожалуйста, /start, ' +
                             'чтобы я добавил вас в список пользователей')
        return 0

    if text == '/start':
        TeleBot.send_message(chat.id, 'Привет. Правила доступны по /rules, ' +
                                      'помощь - по /commands_help')
        USERS[chat.id] = User(chat.id, chat.first_name)

    # /new_situation_NOU_10_60_1_1_help!\nresqueme!\n
    if text.startswith('/new_situation'):
        args = text[13:].split('_')
        try:
            name = args[0]
            danger = int(args[1])
            sit_len = int(args[2])
            freq = int(args[3])
            length = int(args[4])
            texts = args[5].split('\\n')
            stat_time = int(time.time())
            end_time = start_time + sit_len * 60
            sit = Situation(user, danger, start_time, end_time, freq, length, texts, name)
            
            SITUATIONS.append(sit)
            TeleBot.send_message(chat.id, 'Ситуация создана!')
        except Exception:
            warn_invalid_args(chat.id)


def main():
    global WORLDS
    global USERS
    WORLDS = {}
    USERS = {}
    TeleBot.polling(interval=3)


if __name__ == "__main__":
    main()
