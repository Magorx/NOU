#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from threading import Thread
import Pingponger
import Tg_interface
import telebot
import time


PP = Pingponger.Pingponger(6319)
token = '779667318:AAFO_3Ptkf2Y7uYstagrckMrBqpt9criQEo'
bot = telebot.TeleBot(token)


@bot.message_handler(func=lambda x: True)
def recieve_message(message):
    PP.interfaces['telegram'].handle(message)


def launch_tg_bot(bot):
    print('Starting telegram bot')
    bot.polling(interval=1)
    print('Telegram bot shut down')


def everysecond_check():
    t = 0
    while True:
        t += 1
        if t % 10 == 0:
            print('[{}]Checking is OK.'.format(int(time.time())))
        PP.check_situations()
        time.sleep(1)


def main():
    global PP
    print('Starting PingPonger, current time = {}'.format(int(time.time())))

    PP.add_interface('telegram', Tg_interface.TgBot(PP, 'TgBot', bot))

    tg_bot_thread = Thread(target=launch_tg_bot, args=(bot,))
    tg_bot_thread.start()

    everysecond_check_thread = Thread(target=everysecond_check)
    everysecond_check_thread.start()


if __name__ == "__main__":
    main()