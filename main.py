#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from threading import Thread
import Pingponger
import Tg_interface
import telebot


PP = Pingponger.Pingponger(6319)
token = '779667318:AAFO_3Ptkf2Y7uYstagrckMrBqpt9criQEo'
bot = telebot.TeleBot(token)


@bot.message_handler(func=lambda x: True)
def recieve_message(message):
    PP.text_dump()
    PP.interfaces['telegram'].handle(message)


def launch_tg_bot(bot):
    print('Starting telegram bot')
    bot.polling(interval=1)
    print('Telegram bot shut down')



def main():
    global PP

    PP.add_interface('telegram', Tg_interface.TgBot(PP, 'TgBot', bot))

    tg_bot_thread = Thread(target=launch_tg_bot, args=(bot,))
    tg_bot_thread.start()


if __name__ == "__main__":
    main()